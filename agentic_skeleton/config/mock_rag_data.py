# filepath: /Workspace/Hackathon/AgenticSkeleton/agentic_skeleton/config/mock_rag_data.py
"""
Mock RAG Database
=================

Contains a dictionary simulating a Retrieval-Augmented Generation (RAG)
database for various banking topics relevant to a large UK bank (themed like Lloyds).

Each topic includes:
- keywords: Terms likely to appear in user queries related to the topic.
- context: A brief description of the service or topic.
- offers: Potential promotional offers or benefits related to the topic.
- tips: Advice or best practices for colleagues regarding the topic.
- related_docs: Links or references to internal documents or resources.
"""

MOCK_RAG_DB = {
    # --- Mortgages ---
    "first_time_buyer_mortgage": {
        "keywords": ["first time buyer", "ftb", "mortgage", "help to buy", "deposit", "home loan", "property ladder"],
        "context": "Lloyds Bank offers specialized mortgages for First Time Buyers, including options with smaller deposits and guidance through the home buying process. We support government schemes like Help to Buy ISA (closed to new applicants but manageable for existing holders) and potentially Shared Ownership.",
        "offers": [
            "Fee-saver options available on selected FTB mortgages.",
            "Access to our Home Buying Guide and expert Mortgage Advisers.",
            "Potential cashback offers on completion (check current promotions).",
            "Free standard valuation on selected products."
        ],
        "tips": [
            "Advise clients to check their credit score early.",
            "Explain the different types of mortgages clearly (fixed, tracker, variable).",
            "Highlight the importance of saving for associated costs (stamp duty, legal fees).",
            "Direct clients to our online affordability calculator.",
            "Emphasize the support available from our Mortgage Advisers."
        ],
        "related_docs": [
            "FTB Mortgage Product Guide (doc_id: LBM_FTB001)",
            "Home Buying Process Guide (link: /intranet/mortgages/ftb-guide)",
            "Current Mortgage Rates Sheet (doc_id: LBM_RATES0425)",
            "Affordability Calculator (tool: /tools/mortgage-affordability)"
        ]
    },
    "remortgaging": {
        "keywords": ["remortgage", "switch mortgage", "new deal", "lower payments", "equity release", "borrow more"],
        "context": "Lloyds Bank provides remortgaging options for existing homeowners looking to switch their deal, potentially lower monthly payments, or borrow additional funds against their property equity.",
        "offers": [
            "No legal fees or standard valuation fees on many remortgage products.",
            "Competitive fixed and tracker rates available.",
            "Dedicated support from our remortgage specialists.",
            "Online remortgage application portal for ease."
        ],
        "tips": [
            "Check the client's current mortgage terms for any Early Repayment Charges (ERCs).",
            "Discuss the client's goals: saving money, borrowing more, or changing terms.",
            "Explain the difference between switching rates internally vs. a full remortgage.",
            "Use the 'Borrow More' calculator for clients needing additional funds.",
            "Advise clients to start the process 2-3 months before their current deal ends."
        ],
        "related_docs": [
            "Remortgage Product Options (doc_id: LBM_REMORT002)",
            "Remortgage Process Overview (link: /intranet/mortgages/remortgage-process)",
            "Borrow More Calculator (tool: /tools/borrow-more)",
            "Early Repayment Charge Guide (doc_id: LBM_ERC001)"
        ]
    },
    "buy_to_let_mortgage": {
        "keywords": ["buy to let", "btl", "landlord", "investment property", "rental income"],
        "context": "Lloyds Bank offers Buy-to-Let mortgages for individuals looking to purchase or remortgage residential properties for rental purposes. Specific criteria regarding rental income and applicant status apply.",
        "offers": [
            "Range of BTL mortgage products for purchase and remortgage.",
            "Support for experienced landlords and those new to BTL.",
            "Access to resources on landlord responsibilities."
        ],
        "tips": [
            "Ensure the client understands the risks and responsibilities of being a landlord.",
            "Verify the property meets rental income coverage ratios.",
            "Explain the tax implications of rental income (advise seeking independent advice).",
            "Discuss portfolio landlord criteria if applicable.",
            "Highlight the importance of landlord insurance (can refer to insurance team)."
        ],
        "related_docs": [
            "BTL Mortgage Criteria (doc_id: LBM_BTL003)",
            "Landlord Responsibilities Guide (link: /intranet/btl/landlord-info)",
            "Rental Income Calculator (tool: /tools/btl-rental-calc)",
            "Portfolio Landlord Policy (doc_id: LBM_PORTFOLIO01)"
        ]
    },

    # --- General Banking --- 
    "current_accounts": {
        "keywords": ["current account", "bank account", "debit card", "overdraft", "switching", "club lloyds"],
        "context": "Lloyds Bank offers a range of current accounts to suit different needs, from basic banking to accounts with added benefits like Club Lloyds, which provides rewards and lifestyle perks.",
        "offers": [
            "Switching incentives often available via the Current Account Switch Service (CASS).",
            "Club Lloyds benefits (e.g., cinema tickets, magazine subscription, fee-free debit card use abroad - check terms).",
            "Arranged overdraft options available (subject to status).",
            "Mobile Banking app with features like spending insights and saving goals."
        ],
        "tips": [
            "Use the account comparison tool to help customers choose the right account.",
            "Explain the eligibility criteria and funding requirements for Club Lloyds.",
            "Clearly explain overdraft fees and interest rates.",
            "Promote the ease and security of the CASS.",
            "Highlight the features of the Mobile Banking app."
        ],
        "related_docs": [
            "Current Account Comparison (link: /intranet/banking/current-accounts)",
            "Club Lloyds Terms & Benefits (doc_id: LBC_CLUB001)",
            "Overdraft Information & Calculator (tool: /tools/overdraft-info)",
            "Current Account Switch Service Guide (doc_id: LBC_CASS01)",
            "Mobile Banking App Features (link: /intranet/digital/mobile-app)"
        ]
    },
    "savings_accounts": {
        "keywords": ["savings", "isa", "fixed rate bond", "easy access", "interest rate", "saving goals"],
        "context": "Lloyds Bank provides various savings accounts and ISAs (Individual Savings Accounts) to help customers grow their money, including easy access, fixed-rate bonds, and tax-efficient ISAs.",
        "offers": [
            "Competitive interest rates on different account types (check current rates).",
            "Tax-free savings options with Cash ISAs and Stocks & Shares ISAs (referral needed for S&S).",
            "Fixed Rate Bonds for guaranteed returns over a set term.",
            "Easy access accounts for flexibility."
        ],
        "tips": [
            "Discuss the customer's savings goals and timeframe.",
            "Explain the difference between AER and Gross interest rates.",
            "Clarify ISA rules and annual allowances.",
            "Explain the access restrictions on Fixed Rate Bonds.",
            "Promote setting up regular savings plans."
        ],
        "related_docs": [
            "Savings Account Options (link: /intranet/savings/account-types)",
            "Current Savings & ISA Rates (doc_id: LBS_RATES0425)",
            "ISA Guide (doc_id: LBS_ISA002)",
            "Fixed Rate Bond Terms (doc_id: LBS_FRB005)",
            "Savings Goal Planner (tool: /tools/savings-planner)"
        ]
    },

    # --- Credit Cards ---
    "credit_card_types": {
        "keywords": ["credit card", "mastercard", "visa", "balance transfer", "purchase card", "rewards card", "low rate", "credit builder"],
        "context": "Lloyds Bank offers a variety of credit cards designed for different purposes, such as balance transfers, everyday purchases, earning rewards, or building credit history.",
        "offers": [
            "Promotional 0% interest periods on balance transfers or purchases (check specific card offers).",
            "Rewards points or cashback on selected cards.",
            "Cards designed for those new to credit or looking to improve their score.",
            "Competitive standard interest rates (APR)."
        ],
        "tips": [
            "Use the eligibility checker before applying to avoid impacting credit score unnecessarily.",
            "Explain how balance transfers work, including any fees.",
            "Highlight the benefits of the specific rewards program if applicable.",
            "Emphasize the importance of paying on time and preferably more than the minimum payment.",
            "Explain what APR means and how interest is calculated."
        ],
        "related_docs": [
            "Credit Card Comparison (link: /intranet/cards/compare-cards)",
            "Eligibility Checker (tool: /tools/card-eligibility)",
            "Balance Transfer Guide (doc_id: LBCR_BT001)",
            "Rewards Program Details (link: /intranet/cards/rewards)",
            "Understanding APR and Credit (doc_id: LBCR_CREDIT101)"
        ]
    },

    # --- Finance & Loans ---
    "personal_loans": {
        "keywords": ["loan", "personal loan", "borrow money", "debt consolidation", "home improvement loan", "car loan"],
        "context": "Lloyds Bank offers unsecured personal loans for various purposes like debt consolidation, car purchase, or home improvements, with fixed monthly payments.",
        "offers": [
            "Competitive APRs based on loan amount and personal circumstances.",
            "Quick decision and funds transfer possible for eligible applicants.",
            "Flexible loan terms available.",
            "Option to make overpayments."
        ],
        "tips": [
            "Use the loan calculator to estimate monthly payments.",
            "Ensure the customer understands it's a fixed-term commitment.",
            "Explain the difference between representative APR and personal APR.",
            "Discuss the purpose of the loan to ensure it's appropriate.",
            "Advise customers to only borrow what they can afford to repay."
        ],
        "related_docs": [
            "Personal Loan Details (link: /intranet/loans/personal-loan)",
            "Loan Calculator (tool: /tools/loan-calculator)",
            "Loan Application Guide (doc_id: LBL_APP001)",
            "Understanding APR (doc_id: LBL_APR01)"
        ]
    },

    # --- Car Leasing / Finance ---
    "car_finance_leasing": {
        "keywords": ["car finance", "car loan", "pcp", "personal contract purchase", "hire purchase", "hp", "car leasing", "lex auto"],
        "context": "Lloyds Bank offers car finance options like Hire Purchase (HP) and Personal Contract Purchase (PCP). Additionally, through partners like Lex Autolease, we facilitate vehicle leasing solutions.",
        "offers": [
            "Competitive rates on HP and PCP agreements.",
            "Flexible deposit and term options.",
            "Access to a wide range of vehicles through leasing partners.",
            "Online tools to compare finance options."
        ],
        "tips": [
            "Explain the key differences between HP (ownership at end) and PCP (options at end: pay balloon, return, part-ex).",
            "Clarify mileage restrictions and condition requirements for PCP and leasing.",
            "Direct customers to Lex Autolease or relevant partner sites for specific leasing quotes.",
            "Ensure customers understand the total amount payable for finance options.",
            "Discuss the pros and cons of financing vs. leasing based on customer needs."
        ],
        "related_docs": [
            "Car Finance Options Explained (link: /intranet/finance/car-finance)",
            "HP vs PCP Comparison (doc_id: LBF_HPvPCP01)",
            "Lex Autolease Partner Portal (link: external/lex-autolease)",
            "Car Finance Calculator (tool: /tools/car-finance-calc)"
        ]
    },

    # --- Small & Medium Business (SMB) ---
    "business_bank_accounts": {
        "keywords": ["business account", "smb banking", "sme account", "sole trader", "limited company", "business banking"],
        "context": "Lloyds Bank provides business bank accounts tailored for different types of businesses, from sole traders and start-ups to established SMEs, offering features to manage business finances effectively.",
        "offers": [
            "Introductory periods of free banking for new businesses (check current offers).",
            "Access to Business Internet Banking and Mobile Business Banking app.",
            "Support from our Business Management Team.",
            "Range of accounts based on turnover and transaction needs."
        ],
        "tips": [
            "Identify the business structure (sole trader, partnership, limited company) to recommend the right account.",
            "Explain the account fees after any introductory offer period.",
            "Highlight tools like cash flow forecasting and invoicing partners (if applicable).",
            "Discuss options for taking card payments (referral to merchant services).",
            "Promote the benefits of keeping personal and business finances separate."
        ],
        "related_docs": [
            "Business Account Comparison (link: /intranet/business/accounts)",
            "New Business Offer Details (doc_id: LBB_NEWBIZ01)",
            "Business Banking Fees Tariff (doc_id: LBB_FEES0425)",
            "Guide to Starting a Business (link: /intranet/business/startup-guide)"
        ]
    },
    "business_loans_finance": {
        "keywords": ["business loan", "smb finance", "sme loan", "working capital", "asset finance", "commercial mortgage", "business credit card"],
        "context": "Lloyds Bank offers a range of financing solutions for businesses, including business loans, overdrafts, asset finance, commercial mortgages, and business credit cards to support growth and manage cash flow.",
        "offers": [
            "Term loans for specific investments or expansion.",
            "Flexible business overdrafts for short-term cash flow needs.",
            "Asset finance to acquire vehicles, equipment, or machinery.",
            "Commercial mortgages for purchasing business premises.",
            "Government-backed loan schemes may be available (e.g., Recovery Loan Scheme - check status)."
        ],
        "tips": [
            "Understand the purpose of the finance required (growth, cash flow, asset purchase).",
            "Discuss the different security requirements for various types of finance.",
            "Explain the application process and information needed (business plan, accounts).",
            "Utilize the business loan calculator for estimations.",
            "Refer complex cases to a specialist Business Manager."
        ],
        "related_docs": [
            "Business Finance Options (link: /intranet/business/finance)",
            "Business Loan Calculator (tool: /tools/business-loan-calc)",
            "Asset Finance Guide (doc_id: LBB_ASSETFIN01)",
            "Commercial Mortgage Info (link: /intranet/business/comm-mortgage)",
            "Business Plan Template (doc_id: LBB_BIZPLAN01)"
        ]
    },

    # --- General / Internal ---
    "internal_mobility_program": {
        "keywords": ["internal mobility", "career growth", "job openings", "internal transfer", "promotion", "secondment"],
        "context": "Our Internal Mobility Program facilitates career progression within Lloyds Banking Group, connecting colleagues with new opportunities, roles, and projects across different divisions.",
        "offers": [
            "Access to the internal careers portal with exclusive job listings.",
            "Career development workshops and resources.",
            "Support for secondment opportunities.",
            "Networking events focused on internal career paths."
        ],
        "tips": [
            "Encourage colleagues to keep their internal talent profile updated.",
            "Highlight the benefits of gaining experience in different areas of the bank.",
            "Advise colleagues to have career conversations with their line manager.",
            "Explain the application and interview process for internal roles.",
            "Share success stories of colleagues who have moved internally."
        ],
        "related_docs": [
            "Internal Careers Portal (link: /intranet/careers)",
            "Career Development Framework (doc_id: LBG_CDP001)",
            "Secondment Policy (doc_id: LBG_SECONDMENT01)",
            "Guide to Internal Applications (link: /intranet/careers/apply-guide)"
        ]
    },
    "brand_ambassador_program": {
        "keywords": ["ambassador program", "brand advocacy", "internal promotion", "employee advocacy", "representing lloyds"],
        "context": "The Lloyds Brand Ambassador Program empowers colleagues to confidently and accurately share information about our services, values, and community initiatives, both internally and externally.",
        "offers": [
            "Training modules on key products and bank strategy.",
            "Access to pre-approved content and talking points.",
            "Recognition for active ambassadors in internal communications.",
            "Opportunities to represent Lloyds at certain events (internal/community)."
        ],
        "tips": [
            "Focus on areas you are knowledgeable and passionate about.",
            "Always use approved information and messaging.",
            "Share positive customer experiences (anonymized where necessary).",
            "Understand the program guidelines and compliance requirements.",
            "Connect with other ambassadors to share best practices."
        ],
        "related_docs": [
            "Brand Ambassador Hub (link: /intranet/ambassador)",
            "Program Guidelines (doc_id: LBG_BAP001)",
            "Latest Service Talking Points (link: /intranet/talking-points)",
            "Social Media Policy for Employees (doc_id: LBG_SOCIALMEDIA01)"
        ]
    },
    "digital_banking_security": {
        "keywords": ["online banking security", "mobile app safety", "fraud prevention", "phishing", "scams", "secure login"],
        "context": "Lloyds Bank prioritizes digital banking security. We employ multiple layers of protection for our Online Banking and Mobile App, and provide guidance to customers on how to stay safe from fraud and scams.",
        "offers": [
            "Multi-factor authentication for secure login.",
            "Real-time transaction monitoring and alerts.",
            "Online fraud guarantee (terms apply).",
            "Regular security updates for our digital platforms."
        ],
        "tips": [
            "Advise customers never to share their full PIN, password, or card reader codes.",
            "Educate customers on recognizing phishing emails and smishing texts.",
            "Encourage reporting of suspicious activity immediately.",
            "Highlight the security features within the Mobile App (e.g., biometric login).",
            "Remind customers to keep their contact details up to date for alerts."
        ],
        "related_docs": [
            "Online Security Centre (link: /intranet/security/customer-guidance)",
            "Fraud Prevention Tips (doc_id: LBSec_FraudTips01)",
            "How We Protect You Online (link: /lloydsbank.com/security)",
            "Reporting Suspicious Activity Guide (doc_id: LBSec_Report01)"
        ]
    },

    # --- Insurance ---
    "home_insurance": {
        "keywords": ["home insurance", "buildings insurance", "contents insurance", "property protection", "lloyds home insurance"],
        "context": "Lloyds Bank offers Home Insurance options (underwritten by a partner, e.g., Lloyds Bank General Insurance Limited) covering buildings, contents, or both, with different levels of cover available.",
        "offers": [
            "Combined buildings and contents policies often offer better value.",
            "Optional extras like Accidental Damage, Home Emergency cover.",
            "Discounts may be available for existing Lloyds Bank customers or for buying online (check current promotions)."
        ],
        "tips": [
            "Ensure the customer understands the difference between buildings and contents cover.",
            "Advise accurately calculating the rebuild cost (for buildings) and replacement value (for contents).",
            "Explain policy excesses and exclusions clearly.",
            "Highlight the importance of checking the policy details (IPID, Policy Wording).",
            "Direct customers to the dedicated insurance section/partner site for quotes and full details."
        ],
        "related_docs": [
            "Home Insurance Options (link: /intranet/insurance/home)",
            "Get a Home Insurance Quote (tool: /tools/home-insurance-quote)",
            "Home Insurance Policy Wording [Example] (doc_id: LBGIns_HomePol01)",
            "Insurance Product Information Document (IPID) [Example] (doc_id: LBGIns_HomeIPID01)"
        ]
    },
    "car_insurance": {
        "keywords": ["car insurance", "motor insurance", "vehicle cover", "comprehensive", "third party fire theft", "lloyds car insurance"],
        "context": "Lloyds Bank offers Car Insurance (underwritten by a partner, e.g., BISL Limited) providing comprehensive or third party, fire & theft cover for drivers in the UK.",
        "offers": [
            "Multi-car discounts may be available.",
            "Optional extras like Breakdown Cover, Legal Assistance, Courtesy Car.",
            "Named driver options.",
            "Online portal for policy management."
        ],
        "tips": [
            "Explain the different levels of cover (Comprehensive vs. TPFT).",
            "Advise customers to provide accurate information about the vehicle, drivers, and usage.",
            "Discuss the impact of voluntary excess on the premium.",
            "Explain No Claims Discount (NCD) protection.",
            "Direct customers to the dedicated insurance section/partner site for quotes."
        ],
        "related_docs": [
            "Car Insurance Details (link: /intranet/insurance/car)",
            "Get a Car Insurance Quote (tool: /tools/car-insurance-quote)",
            "Car Insurance Policy Wording [Example] (doc_id: LBGIns_CarPol01)",
            "Car Insurance IPID [Example] (doc_id: LBGIns_CarIPID01)"
        ]
    },

    # --- Investments ---
    "investment_options": {
        "keywords": ["investments", "investing", "stocks and shares", "isa", "investment funds", "financial advice", "wealth management"],
        "context": "Lloyds Bank offers access to investment options, primarily through Stocks & Shares ISAs and Investment Accounts. Financial advice may be available for customers with specific needs (potentially via referral or a wealth division). Note: Standard colleagues cannot give investment advice.",
        "offers": [
            "Stocks & Shares ISA for tax-efficient investing.",
            "General Investment Accounts (GIA).",
            "Access to a range of funds managed by investment partners.",
            "Online investment platform for self-service investors."
        ],
        "tips": [
            "NEVER provide investment advice. Explain that investments can go down as well as up and capital is at risk.",
            "Clearly differentiate between cash savings and investments.",
            "Explain the basic concept of a Stocks & Shares ISA and its tax benefits.",
            "For customers seeking advice or complex products, refer them to the appropriate channel (e.g., Wealth Management, Financial Advice service if available).",
            "Direct self-service customers to the online investment platform and resources."
        ],
        "related_docs": [
            "Introduction to Investing (link: /intranet/investments/intro)",
            "Stocks & Shares ISA Information (link: /intranet/investments/ss-isa)",
            "Investment Platform Access (link: /investments/platform)",
            "Financial Advice Referral Process (doc_id: LBG_FARef01)",
            "Guide to Investment Risk (doc_id: LBG_InvRisk01)"
        ]
    },

    # --- Travel ---
    "travel_money": {
        "keywords": ["travel money", "foreign currency", "exchange rate", "holiday money", "currency exchange", "travel card"],
        "context": "Lloyds Bank offers travel money services, allowing customers to order foreign currency online for collection or delivery, or potentially purchase via branches (check availability). Travel money cards may also be offered.",
        "offers": [
            "Competitive exchange rates, especially for popular currencies.",
            "Order online for home delivery or branch collection.",
            "Buy back guarantee option may be available.",
            "Fee-free transactions abroad on certain debit/credit cards (check specific product T&Cs)."
        ],
        "tips": [
            "Advise customers to order currency in advance, especially for less common currencies.",
            "Explain how exchange rates work and that they fluctuate.",
            "Highlight the security benefits of using cards abroad compared to carrying large amounts of cash.",
            "Check branch availability for 'on-demand' currency.",
            "Mention any associated fees for delivery or card usage abroad."
        ],
        "related_docs": [
            "Travel Money Service (link: /intranet/travel/currency)",
            "Order Foreign Currency Online (tool: /tools/travel-money-order)",
            "Current Exchange Rates (link: /intranet/travel/rates)",
            "Using Your Card Abroad Guide (doc_id: LBC_CardAbroad01)"
        ]
    },

    # --- Customer Service ---
    "complaints_handling": {
        "keywords": ["complaint", "issue", "problem", "unhappy", "feedback", "customer service issue", "resolve problem"],
        "context": "Lloyds Bank has a formal complaints procedure to address customer dissatisfaction. Colleagues should aim to resolve issues at the first point of contact where possible, or escalate appropriately following the defined process.",
        "offers": [
            "Dedicated channels for logging complaints (phone, online form, branch).",
            "Acknowledgement of complaint within specified timeframe.",
            "Investigation by a dedicated complaints team if not resolved initially.",
            "Access to the Financial Ombudsman Service (FOS) if the customer remains dissatisfied after our final response."
        ],
        "tips": [
            "Listen empathetically to the customer's concerns.",
            "Apologize for the customer's experience (without necessarily admitting liability initially).",
            "Gather all relevant information about the issue.",
            "Explain the complaints process and expected timelines.",
            "Log the complaint accurately in the system.",
            "If empowered, offer appropriate resolution within guidelines; otherwise, escalate correctly."
        ],
        "related_docs": [
            "Complaints Handling Procedure (link: /intranet/compliance/complaints)",
            "Complaint Logging System (tool: /tools/complaint-logger)",
            "Customer Resolution Framework (doc_id: LBG_CRF01)",
            "Financial Ombudsman Service Information (link: /intranet/compliance/fos)"
        ]
    }
}
