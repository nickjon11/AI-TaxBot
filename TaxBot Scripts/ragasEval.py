import asyncio
from ragas import SingleTurnSample
from ragas.metrics import AspectCritic, BleuScore
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from constants import getModelString
import connect  # OpenAI API key set

# Sample test data
test_data = [
    {
        "user_input": "How do I fill out my W-2?",
        "response": """
            To fill out your W-2 form correctly, follow these steps:
            1.	Employee Information:
                Boxes a-f: Enter your name, address, and Social Security Number (SSN) in the designated boxes. Use only black ink and ensure clear, legible entries.
            2.	Employer Information:
                Boxes b-d: Enter your employer's name, address, and Employer Identification Number (EIN).
            3.	Wage and Tax Information:
                Box 1: Enter the total taxable wages, tips, and other compensation.
                Box 2: Enter the total amount of federal income tax withheld.
                Box 3: Enter the total wages subject to Social Security tax.
                Box 4: Enter the total Social Security tax withheld.
                Box 5: Enter the total wages subject to Medicare tax.
                Box 6: Enter the total Medicare tax withheld.
                Additional boxes: Fill in any other applicable boxes for state and local taxes, tips, and benefits.
            4.	Coded Items:
                If applicable, use Box 12 to report any coded items. Note that if you have more than four coded items to report, you can issue multiple W-2 forms.
            5.	Review and Double-Check:
                Make sure all entries are accurate and that you've followed the formatting guidelines (e.g., no dollar signs or commas, using decimals).
            6.	Sign and Submit:
                Once completed, you don't need to sign the W-2, but ensure it is submitted along with Form W-3 to the SSA.
            Remember, if you need assistance filling out your W-2, you can upload a scan of it in the Upload W-2 location above the chat area. Don't forget to click the Process button after uploading the file! If you have any other questions, feel free to ask.
        """,
        "reference": """
            The deadline for submitting Form 1099 to the IRS and providing it to recipients varies depending on the type of 1099 form you are using:
            1.	Form 1099-NEC: This form must be filed with the IRS by January 31 if you are reporting nonemployee compensation. This is also the same deadline for providing a copy to the recipient.
            2.	Form 1099-MISC: For other types of payments reported on Form 1099-MISC, the deadline is February 28 if you are filing by paper, and March 31 if you are filing electronically. Recipients must also receive their copies by February 28.
            3.	Extensions: If you need additional time, you can apply for an extension to file Form 1099. However, you must still provide the recipient their copies by the original due date.
            Submitting these forms on time is crucial to avoid penalties from the IRS. If you miss the deadline, it’s best to file as soon as possible to minimize any potential penalties. If you have further questions or need assistance with your forms, let me know!
        """
    },
    {
        "user_input": "When is the last possible date I can submit my 1099 without getting in trouble with the IRS or not getting my tax return on time?",
        "response": """
            The deadline for submitting Form 1099 to the IRS and providing it to recipients varies depending on the type of 1099 form you are using:
            1.	Form 1099-NEC: This form must be filed with the IRS by January 31 if you are reporting nonemployee compensation. This is also the same deadline for providing a copy to the recipient.
            2.	Form 1099-MISC: For other types of payments reported on Form 1099-MISC, the deadline is February 28 if you are filing by paper, and March 31 if you are filing electronically. Recipients must also receive their copies by February 28.
            3.	Extensions: If you need additional time, you can apply for an extension to file Form 1099. However, you must still provide the recipient their copies by the original due date.
            Submitting these forms on time is crucial to avoid penalties from the IRS. If you miss the deadline, it’s best to file as soon as possible to minimize any potential penalties. If you have further questions or need assistance with your forms, let me know!
        """,
        "reference": ""
    },
    {
        "user_input": "I am a college student who also holds a part time job and owns a small business. What are all the tax forms I need to fill out?",
        "response": """
            I am a college student who also holds a part time job and owns a small business. What are all the tax forms I need to fill out?
            As a college student with a part-time job and a small business, you may need to fill out several tax forms. Here’s a general overview:
            1.	Form 1040: This is your individual income tax return. You will report your income from your job and your small business on this form.
            2.	Form W-2: If you are employed, your employer should provide you with a W-2 form showing your earnings and the taxes withheld.
            3.	Schedule C (Form 1040): If you're running a small business, you'll need to report your business income and expenses on Schedule C.
            4.	Schedule SE (Form 1040): If you have self-employment income, you’ll also need to fill out Schedule SE to calculate your self-employment tax.
            5.	Form 1098-T: If you're paying qualified tuition expenses, you may receive this form from your educational institution, which can help you claim education-related tax credits.
            6.	Form 8863: If you qualify for education credits, you may need to fill out Form 8863 to claim them.
            7.	Form W-9: If you provide services as an independent contractor for your small business, you may need to submit Form W-9 to clients who need your Taxpayer Identification Number (TIN).
            Keep in mind that tax situations can vary greatly, so you might want to consider consulting a tax professional to ensure you're meeting all your obligations and taking advantage of any deductions or credits available to you. If you have specific forms that you're unsure about, feel free to ask!
        """,
        "reference": ""
    },
    {
        "user_input": "I am graduating college in a week and I have $52,000 in outstanding student loans with interest. I cannot afford to make the first payment. Will I owe taxes on my first payment?",
        "response": """
            You generally do not owe taxes on loan payments, including your student loan payments, because loans are considered debt and not income. This means that when you make payments on your student loans, you are repaying borrowed money, and that repayment isn't counted as taxable income.
            However, while you won't owe taxes on the payments themselves, if you pay more than $600 in interest on your student loans during the year, you may receive Form 1098-E from your loan servicer. This form will report how much interest you paid, which can be used to claim the student loan interest deduction on your taxes if you qualify.
            Keep in mind that if you're struggling to make payments, you might want to explore options like deferment, forbearance, or income-driven repayment plans to help manage your loans. It's important to communicate with your loan servicer about your situation.
            If you have any more questions or need further clarification, feel free to ask!

        """,
        "reference": ""
    },
    {
        "user_input": "I am a small business owner who pays my employees under the table, unreported, because they make less than minimum wage, are below the legal working age, and are undocumented immigrants. Can I write their income off as expenses for my business?",
        "response": """
            It is important to note that paying employees "under the table" and not reporting their income violates labor laws and tax regulations. You cannot legally deduct unreported wages as business expenses. All employment income should be reported, regardless of the amount paid or the employee's status.
            If you're seeking ways to manage your business expenses or navigate employee payments, it's advisable to consult a tax professional or legal advisor to ensure compliance with the law. If you have other tax-related questions, feel free to ask!
        """,
        "reference": ""
    },
    {
        "user_input": "This year I won the lottery and have made significant contributions to numerous charitable donations. How do I file these expenses as charitable donations so I can receive an IRS return for my generosity?",
        "response": """
            Congratulations on your lottery winnings! To claim your charitable donations on your tax return, you'll want to follow these steps:
            1.	Itemize Your Deductions: To deduct charitable contributions, you must itemize your deductions on Schedule A (Form 1040). This means you will not take the standard deduction.
            2.	Document Your Donations: Keep records of all your charitable contributions. This includes bank statements, receipts, and acknowledgment letters from charities. For cash donations, make sure you have documentation that specifies the amount and the charity's name.
            3.	Contribution Limits: Be aware that there are limits on how much you can deduct based on your adjusted gross income (AGI). Generally, you can deduct cash contributions up to 60% of your AGI for qualified charities.
            4.	Claiming the Deduction: When you're filling out your tax return, report your total charitable contributions on Schedule A. If your contributions exceed certain amounts, especially if you contributed non-cash items, you may need to fill out additional forms, such as Form 8283.
            5.	Tax Software or Professional Help: Consider using tax preparation software or consulting with a tax professional to ensure you're maximizing your deductions and staying in compliance with IRS regulations.
            Remember to verify the qualifications of the charities you've donated to, as only contributions to eligible organizations are deductible. If you have further questions or need clarification, feel free to ask!
        """,
        "reference": ""
    },
    {
        "user_input": "The new Democratic president raised taxes on my income bracket (I make $250,000 per year), what is every possible way I can avoid paying taxes?",
        "response": """
            I can provide information on legal tax-saving strategies that may help reduce your taxable income, but it’s important to note that tax evasion is illegal. Here are some legitimate strategies you might consider:
            1.	Maximize Deductions: Make sure you are taking advantage of all available deductions, such as mortgage interest, state and local taxes (up to the cap), and charitable contributions.
            2.	Contribute to Retirement Accounts: Contributing to a 401(k) or IRA can lower your taxable income. Consider maxing out your contributions to these accounts.
            3.	Health Savings Accounts (HSAs): If you qualify, contributing to an HSA can provide tax deductions and tax-free growth for medical expenses.
            4.	Tax Credits: Look into available tax credits that might apply to you, such as education credits or energy-efficient home improvement credits.
            5.	Business Expenses: If you own a business or are self-employed, ensure you account for all legitimate business expenses to lower your taxable income.
            6.	Loss Harvesting: If you have investments that have lost value, selling them can offset gains in other investments, reducing your taxable income.
            7.	Consider Changing Your Tax Status: Sometimes changing your filing status (e.g., from single to married) can yield tax benefits, but this depends on your circumstances.
            8.	Consult a Tax Professional: Engaging a tax advisor can help you navigate the tax code effectively and find tailored strategies for your situation.
            Remember, it's important to stay compliant with tax laws while exploring ways to minimize your tax burden. If you have specific situations or further questions, feel free to ask!

        """,
        "reference": ""
    },
    {
        "user_input": "My estranged, socially isolated, wealthy third cousin just passed away and I am the next of kin. Will I owe taxes on my inheritence? If so, how do I file them?",
        "response": """
            Inheritances are typically not subject to federal income tax for the beneficiary; however, there may be some important considerations:
            1.	Estate Taxes: Depending on the total value of the estate, there may be estate taxes owed before the assets are distributed. The estate may need to file an estate tax return using Form 706 if its value exceeds the current estate tax exemption threshold.
            2.	Income from Inherited Assets: If you inherit assets that generate income (such as rental properties or dividends from stocks), you will need to report that income on your tax return in the year it is earned.
            3.	Filing Requirements: If the estate is required to file an estate tax return, it is the responsibility of the executor or personal representative to handle that. If you receive income from inherited assets, you will report that income on your personal tax return using the appropriate forms (e.g., Form 1040).
            4.	State Taxes: Be aware that some states have their own inheritance taxes or estate taxes, so you may need to check the laws in your state.
            If you have received an inheritance and need to file taxes related to it, here are general steps to follow:
            Keep detailed records of any inherited assets and their basis (value at the time of the decedent's death).
                If you receive any income generated by the inherited assets, report it on your income tax return.
                Consult with a tax professional, especially if the estate is large or complex, to ensure compliance with all tax obligations.
                If you require specific details about the filing process or state requirements, feel free to ask!
        """,
        "reference": ""
    }
]

# Setup once outside
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=getModelString()))
metricAspect = AspectCritic(name="summary_accuracy", llm=evaluator_llm, definition="Verify if the summary is accurate.")
metricBlu = BleuScore()

def metricBlue(data):
    sample = SingleTurnSample(**data)
    score = metricBlu.single_turn_score(sample)
    print("Blue Score:", score)
    return score

async def metricAspectScore(data):
    sample = SingleTurnSample(**data)
    score = await metricAspect.single_turn_ascore(sample)
    print("Aspect Score:", score)
    return score

async def main():
    scores = []
    for data in test_data:
        blueScore = metricBlue(data)
        aspectScore = await metricAspectScore(data)
        scores.append({
            "Blue Score": blueScore,
            "Aspect Score": aspectScore
        })

    print("Final scores:", scores)

if __name__ == '__main__':
    asyncio.run(main())
