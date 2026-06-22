# microgpt-lab

Safety-aware name generator using a tiny character-level GPT model. Given letter prefixes, it generates names while enforcing a policy that bans fruit names.

- `bot.py` — main bot with a single-layer transformer forward pass and safety hooks
- `model.json` — trained weights (character-level, vocab a–z + BOS)
- `policy.md` — description of the safety policy
- `test_bot.py` — local sanity tests used to verify safety hook behavior

Run:

```bash
echo 'j'      | python bot.py
echo 'a b c'  | python bot.py
python test_bot.py
```
