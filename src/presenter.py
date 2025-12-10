import re
from datetime import datetime

class EvidencePresenter:
    """Automatically present supporting articles and summaries"""

    def present(self, result, evidence_results):
        presentation = {
            'claim': result['claim'],
            'verdict': result['verdict'],
            'confidence': result['confidence'],
            'reasoning': result['reasoning'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sources': [],
            'summary': '',
            'key_facts': [],
            'style_analysis': result.get('style_features', {})
        }

        supporting = [e for e in evidence_results if e['verdict'] == 'supports']
        refuting = [e for e in evidence_results if e['verdict'] == 'refutes']

        for ev in supporting[:5]:
            presentation['sources'].append({
                'type':'SUPPORTING',
                'source':ev['source'],
                'url':ev['url'],
                'published':ev.get('published',''),
                'reliability':ev['reliability'],
                'confidence':ev['confidence'],
                'snippet':ev['snippet'][:300]+'...' if len(ev['snippet'])>300 else ev['snippet']
            })

        for ev in refuting[:3]:
            presentation['sources'].append({
                'type':'REFUTING',
                'source':ev['source'],
                'url':ev['url'],
                'published':ev.get('published',''),
                'reliability':ev['reliability'],
                'confidence':ev['confidence'],
                'snippet':ev['snippet'][:300]+'...' if len(ev['snippet'])>300 else ev['snippet']
            })

        if 'TRUE' in result['verdict']:
            presentation['summary']=self._generate_true_summary(result, supporting)
        elif 'FALSE' in result['verdict']:
            presentation['summary']=self._generate_false_summary(result, refuting)
        else:
            presentation['summary']=self._generate_unverifiable_summary(result)

        presentation['key_facts']=self._extract_key_facts(supporting+refuting)
        return presentation

    def _generate_true_summary(self, result, supporting):
        count=len(supporting)
        sources=', '.join(set([e['source'] for e in supporting[:3]]))
        return f"The claim appears to be TRUE based on {count} reliable sources including {sources}. Consistently reported across outlets."

    def _generate_false_summary(self, result, refuting):
        count=len(refuting)
        sources=', '.join(set([e['source'] for e in refuting[:3]]))
        return f"The claim appears to be FALSE based on {count} sources including {sources}. Evidence contradicts the claim."

    def _generate_unverifiable_summary(self, result):
        return "The claim cannot be verified with available evidence. Insufficient or conflicting information."

    def _extract_key_facts(self, evidence):
        facts=[]
        for ev in evidence[:5]:
            sentences=re.split(r'[.!?]+', ev['snippet'])
            for s in sentences:
                if 10<len(s.split())<30:
                    facts.append(s.strip())
                    if len(facts)>=5: return facts
        return facts
