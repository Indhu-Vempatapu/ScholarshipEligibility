import gradio as gr
from experta import *
from experta import Rule, Fact, MATCH, TEST

class ScholarshipEligibility(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.eligible = []
        self.score = 0

    @DefFacts()
    def init(self):
        yield Fact(action='check')

    
  

    # Merit-based: Academic
    @Rule(Fact(action='check'),
        Fact(merit_academic=MATCH.gpa),
        TEST(lambda gpa: gpa is not None and str(gpa).strip() != "" and float(gpa) >= 8.5))
    def merit_academic(self, gpa):
        self.eligible.append("Merit – Academic")
        self.score += 10

    # Merit-based: Research
    @Rule(Fact(action='check'),
        Fact(research=MATCH.research),
        TEST(lambda research: research and research.lower() == 'yes'))
    def merit_research(self, research):
        self.eligible.append("Merit – Research")
        self.score += 10

    # Merit-based: Artistic
    @Rule(Fact(action='check'),
        Fact(artistic=MATCH.artistic),
        TEST(lambda artistic: artistic and artistic.lower() == 'yes'))
    def merit_artistic(self, artistic):
        self.eligible.append("Merit – Artistic")
        self.score += 10

    # Merit-based: Athletic
    @Rule(Fact(action='check'),
        Fact(athletic=MATCH.athletic),
        TEST(lambda athletic: athletic and athletic.lower() == 'yes'))
    def merit_athletic(self, athletic):
        self.eligible.append("Merit – Athletic")
        self.score += 10

    # Need-based
    @Rule(Fact(action='check'),
        Fact(income=MATCH.income),
        TEST(lambda income: income is not None and str(income).strip().isdigit() and int(income) <= 50000))
    def need(self, income):
        self.eligible.append("Need-based")
        self.score += 10

    # International students
    @Rule(Fact(action='check'),
        Fact(international=MATCH.international),
        TEST(lambda x: x and x.lower() == 'yes'))
    def international(self, international):
        self.eligible.append("International")
        self.score += 10

    # Underrepresented: Minority
    @Rule(Fact(action='check'),
        Fact(minority=MATCH.minority),
        TEST(lambda x: x and x.lower() == 'yes'))
    def minority(self, minority):
        self.eligible.append("Underrepresented – Minority")
        self.score += 10

    # Underrepresented: Disability
    @Rule(Fact(action='check'),
        Fact(disability=MATCH.disability),
        TEST(lambda x: x and x.lower() == 'yes'))
    def disability(self, disability):
        self.eligible.append("Underrepresented – Disability")
        self.score += 10

    # Underrepresented: Women in STEM
    @Rule(Fact(action='check'),
        Fact(women_stem=MATCH.women_stem),
        TEST(lambda x: x and x.lower() == 'yes'))
    def women_stem(self, women_stem):
        self.eligible.append("Underrepresented – Women in STEM")
        self.score += 10

    # Underrepresented: First-generation
    @Rule(Fact(action='check'),
        Fact(first_gen=MATCH.first_gen),
        TEST(lambda x: x and x.lower() == 'yes'))
    def first_gen(self, first_gen):
        self.eligible.append("Underrepresented – First-gen")
        self.score += 10

    # Location-specific
    @Rule(Fact(action='check'),
        Fact(location=MATCH.location),
        TEST(lambda loc: loc and loc.strip() != ""))
    def location(self, location):
        self.eligible.append("Location-specific")
        self.score += 5

    # Subject-specific
    @Rule(Fact(action='check'),
        Fact(subject=MATCH.subject),
        TEST(lambda s: s and s.strip() != ""))
    def subject(self, subject):
        self.eligible.append("Subject-specific")
        self.score += 5

    # Institution-specific
    @Rule(Fact(action='check'),
        Fact(provider=MATCH.provider),
        TEST(lambda p: p and p.strip() != ""))
    def provider(self, provider):
        self.eligible.append("Institution-specific")
        self.score += 5

    # Funding type
    @Rule(Fact(action='check'),
        Fact(funding=MATCH.funding),
        TEST(lambda f: f and f.lower() in ["full", "partial", "renewable", "one-time"]))
    def funding(self, funding):
        self.eligible.append(f"{funding.capitalize()} funding")
        self.score += 5


def show_fields(sel):
    updates = []
    updates.append(gr.update(visible="Merit-based" in sel, label="GPA (on a 10-point scale)"))
    updates.append(gr.update(visible="Merit-based" in sel, label="Test scores (e.g. SAT, GRE, etc.)"))
    updates.append(gr.update(visible="Merit-based" in sel, label="Published research? (yes/no)"))
    updates.append(gr.update(visible="Merit-based" in sel, label="Artistic portfolio? (yes/no)"))
    updates.append(gr.update(visible="Merit-based" in sel, label="Athletic achievements? (yes/no)"))

    updates.append(gr.update(visible="Need-based" in sel, label="Annual Family Income (INR)"))
    updates.append(gr.update(visible="International" in sel, label="International student? (yes/no)"))
    updates.append(gr.update(visible="Underrepresented" in sel, label="Minority background? (yes/no)"))
    updates.append(gr.update(visible="Underrepresented" in sel, label="Do you have a disability? (yes/no)"))
    updates.append(gr.update(visible="Underrepresented" in sel, label="Woman in STEM? (yes/no)"))
    updates.append(gr.update(visible="Underrepresented" in sel, label="First-generation college student? (yes/no)"))

    updates.append(gr.update(visible="Location-specific" in sel, label="Home region/country"))
    updates.append(gr.update(visible="Subject-specific" in sel, label="Field of study"))
    updates.append(gr.update(visible="Institution-specific" in sel, label="Scholarship provider"))
    updates.append(gr.update(visible="Funding" in sel, label="Funding type"))

    return updates


def evaluate(sel, gpa, test_scores, research, artistic, athletic,
             income, international, minority, disability,
             women_stem, first_gen, location, subject, provider, funding_input):

    engine = ScholarshipEligibility()
    engine.reset()
    engine.declare(Fact(action='check'))

    is_merit = "Merit-based" in sel
    is_international = "International" in sel or (international and international.lower() == "yes")

    if is_merit:
        if not gpa:
            return "❗ GPA is required for Merit-based scholarships.", ""
        if is_international and not test_scores:
            return "❗ Test scores required for international Merit-based applicants.", ""
        engine.declare(Fact(merit_academic=gpa),
                       Fact(research=research), Fact(artistic=artistic), Fact(athletic=athletic))

    if "Need-based" in sel:
        if income is None:
            return "❗ Income required for Need-based.", ""
        engine.declare(Fact(income=income))

    if "International" in sel:
        if not international:
            return "❗ International status required.", ""
        engine.declare(Fact(international=international))

    if "Underrepresented" in sel:
        engine.declare(Fact(minority=minority or ""),
                       Fact(disability=disability or ""),
                       Fact(women_stem=women_stem or ""),
                       Fact(first_gen=first_gen or ""))

    if "Location-specific" in sel:
        engine.declare(Fact(location=location or ""))
    if "Subject-specific" in sel:
        engine.declare(Fact(subject=subject or ""))
    if "Institution-specific" in sel:
        engine.declare(Fact(provider=provider or ""))
    if "Funding" in sel:
        engine.declare(Fact(funding=funding_input or ""))

    engine.run()
    percent = engine.score
    if engine.eligible:
        return f"✅ Eligible for: {', '.join(engine.eligible)}", f"{percent}%"
    return "❌ Not eligible.", f"{percent}%"


# Launch Gradio app
with gr.Blocks() as app:
    gr.Markdown("### Step 1: Select Scholarship Types")
    types = gr.CheckboxGroup([
        "Merit-based", "Need-based", "International", "Underrepresented",
        "Location-specific", "Subject-specific", "Institution-specific", "Funding"
    ], label="Scholarship Types *")

    gr.Markdown("### Step 2: Answer Required Questions")
    inputs = [
        gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=False),
        gr.Textbox(visible=False), gr.Textbox(visible=False),
        gr.Number(visible=False),
        gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=False),
        gr.Textbox(visible=False), gr.Textbox(visible=False),
        gr.Textbox(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=False),
        gr.Dropdown(["full", "partial", "renewable", "one-time"], visible=False)
    ]
    (gpa, test_scores, research, artistic, athletic,
     income, international, minority, disability,
     women_stem, first_gen, location, subject, provider, funding_input) = inputs

    types.change(fn=show_fields, inputs=[types], outputs=inputs)

    gr.Markdown("### Step 3: Check Eligibility")
    submit = gr.Button("Evaluate")
    result = gr.Textbox(label="Result")
    conf = gr.Textbox(label="Confidence (%)")

    submit.click(fn=evaluate,
                 inputs=[types, gpa, test_scores, research, artistic, athletic,
                         income, international, minority, disability,
                         women_stem, first_gen, location, subject, provider, funding_input],
                 outputs=[result, conf])

app.launch()
