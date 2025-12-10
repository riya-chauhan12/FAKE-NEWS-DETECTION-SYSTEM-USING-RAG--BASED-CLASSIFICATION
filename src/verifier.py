import re, numpy as np
from sentence_transformers import SentenceTransformer

class RAGNLIVerifier:
    def __init__(self):
        print("Loading embedding model (MiniLM, ~80MB)...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ RAG verifier ready")

    def verify(self, claim, evidence):
        sentences = [s.strip() for s in re.split(r'[.!?]+', evidence) if len(s.split())>5]
        if not sentences: return {'verdict':'no_evidence','confidence':0.0,'snippet':''}

        claim_emb=self.embedder.encode([claim])[0]
        sent_embs=self.embedder.encode(sentences[:50])
        similarities=[np.dot(claim_emb,sent_emb)/(np.linalg.norm(claim_emb)*np.linalg.norm(sent_emb)) for sent_emb in sent_embs]
        best_idx=np.argmax(similarities)
        best_sim=float(similarities[best_idx])
        best_sent=sentences[best_idx]
        verdict, confidence=self._analyze(claim,best_sent,best_sim)
        return {'verdict':verdict,'confidence':confidence,'similarity':best_sim,'snippet':best_sent}

    def _analyze(self, claim, sentence, similarity):
        sent_lower=sentence.lower()
        negations=['not','no','never','false','fake','untrue','incorrect','deny','refute','debunk','hoax','myth']
        has_negation=any(neg in sent_lower for neg in negations)
        claim_words=set(re.findall(r'\b\w{3,}\b',claim.lower()))
        sent_words=set(re.findall(r'\b\w{3,}\b',sent_lower))
        overlap=len(claim_words & sent_words)/len(claim_words) if claim_words else 0
        if similarity>0.75:
            return ('refutes', min(similarity+0.1,0.95)) if has_negation and overlap>0.5 else ('supports', min(similarity+0.1,0.95))
        elif similarity>0.6:
            return ('refutes', similarity) if has_negation else ('supports', similarity)
        elif similarity>0.4: return 'supports',0.6
        else: return 'no_evidence', similarity
