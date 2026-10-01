# Translation guide

Maintainer guide for *The Retention Line / Линия Ретенции*. Baseline: Volume I, Chapters 1–4, published 2026-10-01. This file and [GLOSSARY.md](GLOSSARY.md) contain spoilers through Chapter 4. They are repository documentation, not reader-facing pages.

## Authority and scope

The author's current Russian source and explicit corrections govern meaning. The glossary governs established English terminology unless the author changes it or new source evidence requires a documented revision. Earlier English prose is a continuity reference, not authority over the Russian. Do not invent lore to resolve a translation problem.

For new chapters, obtain the full original Google Doc through authorised access. Preserve its body verbatim in `chapters/volume-1-chapter-N.ru.md`, including wording, punctuation, and paragraph boundaries. Separate book, volume, and chapter headings into `book.json`; do not duplicate them in the body. If source formatting or a heading boundary is unclear, inspect the document rather than guessing. Do not correct Russian typos silently. If the author revises a previously published source, review the changes explicitly and update its English counterpart too.

## Voice and prose

- Use natural literary English with British spelling, matching the published baseline: behaviour, metres, grey, stabilisation, organisation. Preserve proper names exactly.
- Preserve the original's dry humour, technical precision, and contrast between bureaucratic language and human stakes. Do not add jokes, explanations, drama, or decorative fantasy diction.
- Keep Kael's precise, analytical voice; Ollan's conversational sarcasm; Mirael's direct authority; and Ilsa's concern. These are tendencies demonstrated in Chapters 1–4, not restrictions on later character development.
- Preserve short fragments, pauses, deliberate repetition, and isolated lines. Do not smooth away the pacing simply to produce conventional paragraphs.
- Preserve uncertainty, qualifications, negation, chronology, numbers, causal direction, and limits on powers. Observation, hypothesis, doctrine, and established fact must remain distinguishable.
- Do not use later revelations to explain earlier ambiguity. In particular, Kael's theory about the Triunity's Gifts is a hypothesis, not confirmed narration. Retention's label does not establish intention, consciousness, or a final mechanism.
- Translate the complete text, without abridgement. Preserve forceful language and emotional intensity at the source's level.

## Terminology and typography

Consult [GLOSSARY.md](GLOSSARY.md) before drafting. Search earlier chapters for the actual use of a recurring phrase. Use established names consistently; do not alternate transliterations or introduce synonyms for named powers.

Capitalise named categories and powers as established: Signature, Ability, Awakening, Gift, Coupling, Anchor, Retention. Use lowercase for ordinary generic language, such as a person's ability to notice something, mana, archē, a circuit, and a retention effect. Match context for Node 7, the Node, and an ordinary node. Use `archē` with its macron; use `Archē` where a title requires it.

Use curly double quotation marks for English dialogue and single quotation marks within dialogue. Keep meaningful emphasis; the English renderer supports `*italics*` and `**bold**`. Russian is rendered as plain text. Do not add unsupported Markdown headings, blockquotes, or lists to chapter bodies. Do not turn ordinary Russian words into capitalised technical terms merely because a glossary entry exists.

Maintain one source body paragraph per English paragraph for new chapters, using a blank line between paragraphs. This supports completeness checks and preserves pacing. If an exceptional restructuring is necessary, document the specific reason; equal paragraph counts alone never prove translation fidelity. Earlier Chapter 1 formatting is a legacy baseline, not permission to omit or combine new material.

## Workflow for each chapter

1. Read this guide, the glossary, the full Russian chapter, and the preceding chapter's ending. Identify new names, technical terms, and repeated warnings or quotations before translating.
2. Preserve the Russian source. Draft the complete English counterpart against that source, consulting established terminology as you go.
3. Review source and translation paragraph by paragraph. Check completeness, speaker attribution, pronouns, negation, quantities, relationships, limitations, humour, and the final paragraph. Check quotations repeated from earlier chapters for continuity while preserving any intentional source changes.
4. Update the glossary in the same change: add the Russian form, English form, category/context, first chapter, and any uncertainty. Use normal words contextually; do not turn the glossary into a mechanical word-substitution table.
5. Add both language titles and source paths to `book.json`. Run `python3 build.py`. Check the original against the retrieved source, paragraph coverage, generated chapter titles, contents, previous/next navigation, language links, and relative links. Existing reader width and display preferences must continue to work.
6. Publish when authorised by the task, then verify the deployed chapter pages in both languages. Report any unresolved translation decisions honestly.

## Changing an established choice

An entry labelled “established” means used in the published English edition; it does not mean separately approved by the author. Keep it unless there is a substantive reason to revise it. Mark a genuinely uncertain new choice as provisional and explain why. Ask the author when competing readings would materially change lore or meaning; routine English phrasing does not require approval.

When a term changes, search all English chapters and `book.json`, review every occurrence in context, update affected passages together, rebuild `docs/`, and record the old form, new form, reason, and affected chapters in the glossary's decision log. Avoid blind global replacement. Never alter Russian originals to accommodate an English terminology change. Keep the glossary and guide current so the next session can resume without relying on chat history.
