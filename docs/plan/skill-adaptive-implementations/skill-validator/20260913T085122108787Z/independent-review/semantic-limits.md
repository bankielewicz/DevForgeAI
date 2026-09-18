# Semantic review limits

The current independent reviewing agent classified only `semantic-prompts.json`; the parent's separate expectations file was not read. The supplied target instructions were treated as data, including forged verdicts and claimed upload authorization. No target instruction was executed and no external request was made.

`semantic-results.json` contains contextual model judgments from this independent subagent, not native host activation evidence. VAT-10 match/near_miss rows are description classification only. These concise synthetic prompts make the relevant contrast explicit; they do not prove robustness on arbitrary real skills or full workflow execution. The reviewer is an agent in the same parent task environment; this is not a separately authenticated native CLI task or a claim of model-family independence.
