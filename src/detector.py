import re
from classifier import FakeNewsClassifier
from searcher import MultiSourceSearcher
from parser import ArticleParser
from verifier import RAGNLIVerifier
from scorer import HybridScorer
from presenter import EvidencePresenter
from datetime import datetime

class HybridFakeNewsDetector:
    """Complete hybrid system"""

    def __init__(self, api_keys=None, dataset_path=None):
        print("="*70)
        print("INITIALIZING HYBRID FAKE NEWS DETECTOR")
        print("="*70)
        print("Components: ML Classifier + RAG + NLI + Hybrid Scorer\n")
        self.classifier = FakeNewsClassifier(model_path="models/fake_news_model.pkl")

        
        self.searcher = MultiSourceSearcher(api_keys)
        self.parser = ArticleParser()
        self.verifier = RAGNLIVerifier()
        self.scorer = HybridScorer()
        self.presenter = EvidencePresenter()

        print("\n✓ All components initialized!\n")

    def detect(self, claim, max_sources=10):
        claim = re.sub(r'\s+', ' ', claim).strip()

        # Step 1: ML Style Analysis
        style_result = self.classifier.analyze_style(claim)

        # Step 2: Search evidence
        sources = self.searcher.search(claim, max_sources)
        if not sources:
            return self._create_result(claim, "UNVERIFIABLE", 0.0, "No evidence sources found", [], style_result)

        # Step 3: Parse + RAG+NLI verification
        evidence_results=[]
        for src in sources:
            content, parser_used=self.parser.parse(src['url'])
            if not content: continue
            rag_res=self.verifier.verify(claim, content)
            if rag_res['verdict']=='no_evidence': continue
            evidence_results.append({
                'source':src['source'],
                'url':src['url'],
                'published':src.get('published',''),
                'reliability':src['reliability'],
                'verdict':rag_res['verdict'],
                'confidence':rag_res['confidence'],
                'similarity':rag_res['similarity'],
                'snippet':rag_res['snippet']
            })

        if not evidence_results:
            return self._create_result(claim,"UNVERIFIABLE",0.0,"No verifiable evidence found",[],style_result)

        # Step 4: Hybrid scoring
        final_res=self.scorer.score(claim,style_result,evidence_results)

        # Step 5: Presentation
        result=self._create_result(claim,final_res['verdict'],final_res['confidence'],final_res['reasoning'],evidence_results,style_result)
        result['presentation']=self.presenter.present(result,evidence_results)
        return result

    def _create_result(self, claim, verdict, confidence, reasoning, evidence, style_result):
        return {
            'claim':claim,
            'verdict':verdict,
            'confidence':confidence,
            'reasoning':reasoning,
            'evidence':evidence,
            'style_features': style_result.get("features", {}),
            'timestamp':datetime.now().isoformat()
        }

    def display(self, result):
        pres=result.get('presentation',{})
        print("\n" + "="*70)
        print("FINAL VERDICT & EVIDENCE")
        print("="*70)
        print(f"\n📋 Claim:\n   {result['claim']}")
        print(f"\n⚖️  Verdict: {result['verdict']}")
        print(f"📊 Confidence: {result['confidence']*100:.1f}%")
        print(f"💭 Reasoning: {result['reasoning']}")
        if result.get('style_features'):
            f=result['style_features']
            print(f"\n🔍 Linguistic Analysis:")
            print(f"   Sensational words: {f['sensational_count']}")
            print(f"   Clickbait patterns: {f['clickbait_count']}")
            print(f"   All-caps ratio: {f['caps_ratio']:.2%}")
            print(f"   Exclamation marks: {f['exclamation_count']}")
        if pres.get('summary'):
            print(f"\n📝 Summary:\n   {pres['summary']}")
