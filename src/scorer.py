class HybridScorer:
    """Combine style, evidence, NLI"""

    def score(self, claim, style_result, evidence_results):
        style_score=style_result['style_score']; style_weight=0.25
        if not evidence_results:
            return {'verdict':'UNVERIFIABLE','confidence':0.0,'reasoning':'No evidence found','scores':{'style':style_score,'evidence':0.0,'nli':0.0}}
        supports_score=refutes_score=0.0; evidence_count={'supports':0,'refutes':0}
        for ev in evidence_results:
            weight=ev['reliability']*ev['confidence']*ev['similarity']
            if ev['verdict']=='supports': supports_score+=weight; evidence_count['supports']+=1
            elif ev['verdict']=='refutes': refutes_score+=weight; evidence_count['refutes']+=1
        total_evidence=supports_score+refutes_score
        evidence_weight=0.5; consistency_score=max(supports_score,refutes_score)/(total_evidence+0.01); nli_weight=0.25

        if supports_score>refutes_score*1.2:
            style_penalty=style_score*0.3
            raw_conf=(1-style_score)*style_weight+(supports_score/(total_evidence+0.01))*evidence_weight+consistency_score*nli_weight-style_penalty
            confidence=max(0.0,min(raw_conf,0.95))
            verdict='TRUE' if confidence>0.70 else 'LIKELY TRUE'
            reasoning=f"Supported by {evidence_count['supports']} sources"
            if style_score>0.6: reasoning+=" (but suspicious language detected)"
        elif refutes_score>supports_score*1.2:
            style_bonus=style_score*0.2
            raw_conf=style_score*style_weight+(refutes_score/(total_evidence+0.01))*evidence_weight+consistency_score*nli_weight+style_bonus
            confidence=max(0.0,min(raw_conf,0.95))
            verdict='FALSE' if confidence>0.70 else 'LIKELY FALSE'
            reasoning=f"Refuted by {evidence_count['refutes']} sources"
        else: verdict='UNVERIFIABLE'; confidence=0.5; reasoning=f"Conflicting evidence ({evidence_count['supports']} support, {evidence_count['refutes']} refute)"

        return {'verdict':verdict,'confidence':confidence,'reasoning':reasoning,'scores':{'style':style_score,'evidence_support':supports_score,'evidence_refute':refutes_score,'consistency':consistency_score},'evidence_count':evidence_count}
