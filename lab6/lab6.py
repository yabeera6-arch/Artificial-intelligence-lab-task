import re, csv, math, time

def show_tokens(text):
    ws, wl = text.split(), re.findall(r"\b\w+\b", text)
    print("Text:", repr(text), "\n  whitespace:", ws, len(ws), "| word-like:", wl, len(wl))

samples = ["AI, search!", "I can't log in.", "help@example.com",
           "CS4944 version 2.1", "", "یہ ایک مثال ہے"]
print("== Task 1: tokenization ==")
for s in samples:
    show_tokens(s)
print("split() keeps punctuation attached (search!), the word regex drops it.")
print("The regex splits can't into can and t, while split() keeps it whole.")
print("Risk: lowercasing or stripping punctuation can damage identifiers like CS4944.")
print()

faq = [
    {"q": "How do I reset my password?", "a": "Use the recovery link on the login page.", "s": "it_help.txt"},
    {"q": "Where do I submit my assignment?", "a": "Upload it through the learning portal.", "s": "assessment.txt"},
    {"q": "Can illness justify a late submission?", "a": "Request an extension with medical evidence before the deadline.", "s": "handbook.txt"},
    {"q": "How do I renew an expired API token?", "a": "Use POST /v2/token/refresh and never print the refresh token in logs.", "s": "api_docs.txt"},
    {"q": "The printer has power but prints blank pages, what now?", "a": "Check ink level, run the cleaning utility, then print a test page.", "s": "troubleshoot.txt"},
]

def answer(query):
    if not query.strip():
        return "Please enter a question."
    for r in faq:
        if query.strip().casefold() == r["q"].casefold():
            return r["a"] + " [source: " + r["s"] + "]"
    qwords = re.findall(r"\w+", query.casefold())
    best, n = None, 0
    for r in faq:
        c = sum(w in re.findall(r"\w+", r["q"].casefold()) for w in qwords)
        if c > n:
            best, n = r, c
    if n == 0:
        return "No matching FAQ. Please contact the help desk."
    return "Possible match, please confirm: " + best["q"]

print("== Task 1: FAQ chatbot ==")
for q in ["How do I reset my password?", "password recovery help", "", "volcano geology"]:
    print("Q:", repr(q), "\nA:", answer(q))
print("The bot asks for confirmation because a similarity score is only a guess, never proof.")
print()
assert "it_help.txt" in answer("How do I reset my password?")
assert answer("") == "Please enter a question."
assert "No matching FAQ" in answer("volcano geology")
assert "Possible match" in answer("password recovery help")

def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    out = []
    for i in range(0, len(spans), size - overlap):
        j = min(i + size, len(spans))
        out.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break
    return out

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    cuts = [0] + [m.end() for m in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    out, pend, cnt = [], None, 0
    for a, b in zip(cuts, cuts[1:]):
        seg = text[a:b]
        n = len(seg.split())
        if not n:
            continue
        if n > size:
            if pend is not None:
                out.append(pend)
            out.extend(windows(seg, size, 0, a))
            pend, cnt = None, 0
        elif pend is not None and cnt + n <= size:
            pend, cnt = (pend[0], b), cnt + n
        else:
            if pend is not None:
                out.append(pend)
            pend, cnt = (a, b), n
    if pend is not None:
        out.append(pend)
    return out

def make_chunks(docs, strategy):
    out = []
    for doc_id, text in docs.items():
        spans = sentence_chunks(text) if strategy == "sentence" else windows(text, 40, int(strategy))
        for i, (a, b) in enumerate(spans):
            out.append({"id": doc_id + ":" + str(i), "doc": doc_id, "start": a, "end": b, "text": text[a:b]})
    return out

handbook = ("Late submission of coursework is normally penalized at ten percent of the total marks for each working day after the deadline. The deadline shown on the learning portal is final, and technical problems on the student side do not remove the penalty. A student who was ill during the submission period may request an extension, but only when valid medical evidence is provided before the original deadline. "
    "The medical certificate must state the dates of illness and must be signed by a registered doctor. Requests made after the deadline without prior notice are rejected automatically. All assignments must be uploaded through the learning portal as a single PDF file. The file name must contain the course code and the student registration number. Email submissions are not accepted under any circumstance, even when the portal is slow, because the portal keeps the official submission record. Students who are unsure about the rules should ask the course coordinator at least two days before the deadline.")

returns = ("For a damaged parcel, the customer must contact the support team within forty eight hours of delivery and attach clear photographs of both the item and the packaging, because claims without photographs cannot be processed and the forty eight hour window is counted from the time shown on the delivery record, not from the time the customer opens the box. The support team will then arrange a replacement or a refund within five working days. For a change of mind, unused items in original packaging can be returned within fourteen days, but the customer pays the return shipping cost. "
    "Items damaged in the other region follow a different policy with a seventy two hour reporting window, so the region shown on the order must be checked before any promise is made. Refunds go back to the original payment method only, and partial refunds are not offered for damaged items that were already discounted. Every claim must include the order number from the confirmation email.")

printer = ("For blank printer pages, follow these steps in order. First, check the ink or toner level on the printer display and replace any empty cartridge. Second, run the printer cleaning utility from the settings menu, because dried ink in the print heads is the most common cause of blank pages when the printer still has power. Third, print a test page to confirm the problem is fixed, and if the test page is still blank after two cleaning cycles, which can happen when the print head is badly clogged or when a third party cartridge is not recognized by the printer firmware, contact the service center instead of repeating the cleaning again and again. "
    "For a blank scanner image, the steps are different: check the document placement on the glass and select the correct scanning source in the software before scanning again. Genuine cartridges are recommended, because third party cartridges sometimes cause faded prints even after cleaning.")

auth = ("Renew an expired API token with POST /v2/token/refresh. Send the refresh_token field in the request body and never print its value in logs. Tokens expire after sixty minutes of issue. The older v1 endpoint POST /v1/auth/renew is removed and now returns an error, so all code must use the v2 endpoint and keep the exact case of refresh_token.")

remote = ("Employees may request remote work with written approval from their manager, and the approval must be renewed every six months. Contractors may work remotely only when the signed contract explicitly permits remote work. Employee remote rules do not apply to contractors under any circumstance. A contractor working remotely without the contract clause is treated as absent.")

docs = {"handbook": handbook, "returns": returns, "printer": printer, "auth": auth, "remote": remote}
corpus2 = {"handbook": handbook, "returns": returns, "printer": printer}

print("== Task 2: chunking edge tests ==")
assert windows("") == []
assert windows("short text") == [(0, 10)]
try:
    windows("a b", 2, 2)
    raise AssertionError("bad overlap accepted")
except ValueError:
    pass
long = " ".join(["word"] * 95) + "."
assert all(len(long[a:b].split()) <= 40 for a, b in sentence_chunks(long))
for c in make_chunks(corpus2, "sentence"):
    assert c["text"] == corpus2[c["doc"]][c["start"]:c["end"]]
print("edge tests passed")

print("== Task 2: strategy comparison ==")
rules = {"handbook": "valid medical evidence is provided before the original deadline",
         "returns": "within forty eight hours of delivery",
         "printer": "run the printer cleaning utility"}
for strat in ["0", "10", "sentence"]:
    chunks = make_chunks(corpus2, strat)
    total = sum(len(c["text"].split()) for c in chunks)
    orig = sum(len(t.split()) for t in corpus2.values())
    kept = sum(1 for d, r in rules.items() if any(c["doc"] == d and r in c["text"] for c in chunks))
    print(strat, "| chunks:", len(chunks), "| repeated words:", total - orig, "| rules kept whole:", kept, "of", len(rules))
print("Sentence splitting fails on abbreviations like e.g. or Mr., which end with a period.")
print("Overlap protects evidence near a boundary but duplicates text and adds work.")
print()

def words(t):
    return re.findall(r"\w+", t.lower())

def build_index(texts):
    n, df, tfs = len(texts), {}, []
    for t in texts:
        tf = {}
        for w in words(t):
            tf[w] = tf.get(w, 0) + 1
        tfs.append(tf)
        for w in set(tf):
            df[w] = df.get(w, 0) + 1
    vocab = sorted(df)
    idf = {w: math.log(n / d) for w, d in df.items()}
    vecs = []
    for tf in tfs:
        v = [tf.get(w, 0) * idf[w] for w in vocab]
        s = math.sqrt(sum(x * x for x in v)) or 1
        vecs.append([x / s for x in v])
    return vocab, idf, vecs

def encode_query(q, vocab, idf):
    tf = {}
    for w in words(q):
        tf[w] = tf.get(w, 0) + 1
    v = [tf.get(w, 0) * idf.get(w, 0) for w in vocab]
    s = math.sqrt(sum(x * x for x in v)) or 1
    return [x / s for x in v]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

queries = [
    ("What proof is needed for an illness extension?", "handbook", "valid medical evidence is provided before the original deadline", "dev"),
    ("My parcel arrived broken, what should I do?", "returns", "within forty eight hours of delivery", "dev"),
    ("Printer has power but the pages are blank", "printer", "run the printer cleaning utility", "dev"),
    ("How do I renew an expired API token?", "auth", "POST /v2/token/refresh", "dev"),
    ("Where do I upload my assignment?", "handbook", "uploaded through the learning portal", "test"),
    ("How can I return an item I changed my mind about?", "returns", "within fourteen days", "test"),
    ("Can contractors work from home?", "remote", "only when the signed contract explicitly permits remote work", "test"),
    ("What happened to the old v1 renew endpoint?", "auth", "is removed", "test"),
    ("What are tomorrow's flight prices?", None, None, "test"),
    ("Who won the football match?", None, None, "test"),
]

def metrics(scores, chunks, items):
    hits, rr = [], []
    for row, q in zip(scores, items):
        if q[1] is None:
            continue
        order = sorted(range(len(row)), key=lambda i: -row[i])[:3]
        good = [r for r, i in enumerate(order, 1) if chunks[i]["doc"] == q[1] and q[2] in chunks[i]["text"]]
        hits.append(bool(good))
        rr.append(1 / good[0] if good else 0)
    return sum(hits) / len(hits), sum(rr) / len(rr)

print("== Task 3: retrieval evaluation (TF-IDF backend) ==")
log, summary, misses = [], {}, []
for strat in ["0", "10", "sentence"]:
    chunks = make_chunks(docs, strat)
    t0 = time.perf_counter()
    vocab, idf, vecs = build_index([c["text"] for c in chunks])
    t1 = time.perf_counter()
    scores = [[dot(encode_query(q[0], vocab, idf), v) for v in vecs] for q in queries]
    t2 = time.perf_counter()
    for split in ["dev", "test"]:
        idx = [i for i, q in enumerate(queries) if q[3] == split]
        h, m = metrics([scores[i] for i in idx], chunks, [queries[i] for i in idx])
        print(strat, split, "| Hit@3:", round(h, 3), "| MRR@3:", round(m, 3), "| chunks:", len(chunks),
              "| encode:", round(t1 - t0, 4), "s | search:", round(t2 - t1, 4), "s")
    kept = sum(1 for q in queries if q[1] and any(c["doc"] == q[1] and q[2] in c["text"] for c in chunks))
    dup = sum(len(c["text"].split()) for c in chunks) - sum(len(t.split()) for t in docs.values())
    summary[strat] = (len(chunks), dup, kept)
    for qi, q in enumerate(queries):
        order = sorted(range(len(scores[qi])), key=lambda i: -scores[qi][i])[:3]
        if strat == "0" and q[1]:
            c0 = chunks[order[0]]
            if not (c0["doc"] == q[1] and q[2] in c0["text"]):
                misses.append((q[0][:40], c0["id"]))
        for rank, i in enumerate(order, 1):
            c = chunks[i]
            log.append({"strategy": strat, "split": q[3], "query": q[0], "rank": rank, "score": round(scores[qi][i], 3),
                        "chunk": c["id"], "start": c["start"], "end": c["end"], "text": c["text"][:90]})
            print(" ", strat, q[3], "rank", rank, c["id"], round(scores[qi][i], 3), c["text"][:75])
with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(log[0]))
    w.writeheader()
    w.writerows(log)
print("wrote retrieval_log.csv with", len(log), "rows")

print("== Task 3: observed failures ==")
for q, cid in misses:
    print("Failure: word windows with no overlap split evidence, so", repr(q), "top hit", cid, "misses it.")
print("Failure:", len(misses), "of 8 answerable queries miss at rank 1 with word windows and zero overlap.")
print("Failure: unanswerable queries still return ranked text, because the highest score only means most similar, not correct.")
print("Failure: paraphrased queries with little shared wording miss under TF-IDF, which cannot see meaning.")
print()

try:
    from sentence_transformers import SentenceTransformer
    t = time.perf_counter()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    print("model load seconds:", round(time.perf_counter() - t, 2))
    for label, text in [("short", "Reset my password."), ("long", "password " * 300)]:
        n = len(model.tokenizer(text, truncation=False)["input_ids"])
        print(label, "tokens:", n, "| limit:", model.max_seq_length, "| fits:", n <= model.max_seq_length)
    print("Model ready; the embedding run can be done on a machine with the download.")
except Exception as e:
    print("No embedding model here (" + type(e).__name__ + "); recorded as a limitation, the TF-IDF evaluation is complete.")

print("== Task 3: strategy choice ==")
for strat, (n, dup, kept) in summary.items():
    print(strat, "| chunks:", n, "| repeated words:", dup, "| evidence kept whole:", kept, "of 8")
print("Choice: sentence-aware packing, because it keeps rules and exceptions whole without repeating text.")

print("== Task 3: document chatbot ==")
def doc_reply(query):
    qv = encode_query(query, vocab, idf)
    ranked = sorted(range(len(chunks)), key=lambda i: -dot(qv, vecs[i]))[:3]
    return [(chunks[i], dot(qv, vecs[i])) for i in ranked]

for q in ["How do I renew an expired API token?", "What are tomorrow's flight prices?"]:
    print("Q:", q, "\nCandidate evidence, please confirm before trusting:")
    for n, (c, s) in enumerate(doc_reply(q), 1):
        print(" ", n, c["id"], round(s, 3), "| chars", c["start"], c["end"], "|", c["text"][:70])
print("Unanswerable queries never get an automatic answer; the bot only shows candidates for the user to inspect.")
print("FAQ matching picks from a fixed question list, while document retrieval searches text chunks, so it can miss surrounding context or mix conflicting sources like the 48 hour and 72 hour region rules.")
