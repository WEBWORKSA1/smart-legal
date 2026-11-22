"""Directory data and legal-page copy."""

PRACTICE_AREAS = ["Personal Injury", "Car / Truck Accident", "Medical Malpractice", "Workers' Compensation", "Family & Divorce",
                  "Child Custody & Support", "Employment", "Housing / Landlord-Tenant", "Immigration", "Criminal Defense", "Traffic / DUI",
                  "Business & Contracts", "Wills & Estates", "Consumer & Debt", "Bankruptcy", "Real Estate", "Intellectual Property",
                  "Privacy & Data", "Social Security / Disability", "Other"]

REGIONS = ["United States", "Canada", "United Kingdom", "India", "Australia", "Ireland", "New Zealand", "European Union",
           "United Arab Emirates", "Singapore", "Other"]

LEGAL_AID = {
 "United States": [
  ("Legal Services Corporation — find legal aid", "https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help", "Federally funded civil legal aid, searchable by location."),
  ("LawHelp.org", "https://www.lawhelp.org/", "State-by-state directory of non-profit legal aid and self-help guides."),
  ("ABA Free Legal Answers", "https://www.abafreelegalanswers.org/", "Free online civil legal questions answered by volunteer lawyers (eligibility applies)."),
  ("LawHelp Interactive", "https://www.lawhelpinteractive.org/", "Free guided interviews that complete court forms."),
  ("USA.gov — legal aid", "https://www.usa.gov/legal-aid", "Official federal guide to free and low-cost legal help."),
  ("Cornell LII", "https://www.law.cornell.edu/", "Free access to US federal and state law."),
 ],
 "Canada": [
  ("Legal Aid Ontario", "https://www.legalaid.on.ca/", "Ontario's legal aid programme for eligible residents."),
  ("Commission des services juridiques (Québec)", "https://www.csj.qc.ca/", "Legal aid for eligible Quebec residents."),
  ("Éducaloi", "https://educaloi.qc.ca/en/", "Plain-language legal information for Quebec."),
  ("Legal Aid BC", "https://legalaid.bc.ca/", "Legal aid and family-law resources in British Columbia."),
  ("Department of Justice — legal aid", "https://www.justice.gc.ca/eng/fund-fina/gov-gouv/aid-aide.html", "Federal overview of legal aid across provinces and territories."),
  ("CanLII", "https://www.canlii.org/", "Free Canadian case law and legislation."),
 ],
 "United Kingdom": [
  ("Check if you can get legal aid (GOV.UK)", "https://www.gov.uk/check-legal-aid", "Official eligibility checker for England and Wales."),
  ("Citizens Advice", "https://www.citizensadvice.org.uk/", "Free, confidential advice on work, housing, debt and more."),
  ("Find a legal adviser (GOV.UK)", "https://www.gov.uk/find-a-legal-adviser", "Search legal aid providers."),
  ("LawWorks", "https://www.lawworks.org.uk/", "Pro bono legal advice clinics."),
  ("Scottish Legal Aid Board", "https://www.slab.org.uk/", "Legal aid in Scotland."),
 ],
 "India": [
  ("National Legal Services Authority (NALSA)", "https://nalsa.gov.in/", "Free legal services under the Legal Services Authorities Act."),
  ("Tele-Law (Department of Justice)", "https://www.tele-law.in/", "Free pre-litigation advice through video and phone."),
  ("eCourts Services", "https://ecourts.gov.in/", "Case status and court information."),
  ("India Code", "https://www.indiacode.nic.in/", "Official repository of central and state Acts."),
 ],
 "Australia": [
  ("National Legal Aid", "https://www.nationallegalaid.org/", "Links to legal aid commissions in each state and territory."),
  ("Community Legal Centres Australia", "https://clcs.org.au/", "Find a free community legal centre."),
  ("Legal Aid NSW", "https://www.legalaid.nsw.gov.au/", "Legal aid for New South Wales residents."),
  ("Victoria Legal Aid", "https://www.legalaid.vic.gov.au/", "Legal aid for Victorian residents."),
 ],
 "International": [
  ("UNHCR — help for refugees", "https://help.unhcr.org/", "Country-specific information for refugees and asylum seekers."),
  ("International Legal Foundation", "https://www.theilf.org/", "Public defence for people who cannot afford a lawyer in several countries."),
  ("Pro bono clearing houses (TrustLaw)", "https://www.trust.org/trustlaw/", "Connects NGOs and social enterprises with free legal assistance."),
 ],
}

def privacy_body():
    return """
<p>This Privacy Policy explains how Smart.Legal ("we", "us") collects, uses and shares information when you visit smart.legal (the "Site").</p>
<h2>1. Information you give us</h2><p>When you submit a form — free case review, legal question, newsletter, donation pledge, contest entry, job application, partner or contact form — we receive the information you enter, such as your name, email, phone number, location and description of your matter. Do not submit highly sensitive information you do not want shared with the people who will respond to your request.</p>
<h2>2. How we use it</h2><ul><li>To respond to your request and, for case reviews, to share it with independent attorneys, legal-service partners or legal-aid organisations that may be able to help you in your area.</li><li>To send newsletters you asked for (you can unsubscribe at any time).</li><li>To run contests, process applications, sponsorships and donation pledges.</li><li>To improve and secure the Site and create anonymous content from questions.</li></ul>
<p>We do not sell your personal information for money. Sharing case-review details with partners at your request is part of the service you asked for.</p>
<h2>3. Tools run in your browser</h2><p>The Navigator, document generator, calculators, dictionary search and quiz process what you type locally in your browser. That information is not sent to us unless you submit a form.</p>
<h2>4. Form processing</h2><p>Forms are delivered to our inbox through a third-party form-relay service, which processes submissions on our behalf to deliver them by email.</p>
<h2>5. Cookies and advertising</h2><p>We use cookies and similar technologies to remember preferences (such as dark mode), measure use of the Site and show advertising.</p>
<ul><li>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites.</li><li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this Site and/or other sites on the Internet.</li><li>You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a> and <a href="https://www.youronlinechoices.eu/" target="_blank" rel="noopener">youronlinechoices.eu</a>.</li><li>Learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>.</li></ul>
<p>Visitors in the EEA, UK and Switzerland are shown a consent message where required before personalised ads are served.</p>
<h2>6. Embedded content</h2><p>Videos are embedded from YouTube using privacy-enhanced mode and load only when you press play. News headlines link to external publishers whose own policies apply.</p>
<h2>7. Your rights</h2><p>Depending on where you live (for example under the GDPR, UK GDPR, CCPA/CPRA, PIPEDA or India's DPDP Act), you may have rights to access, correct, delete or port your information, to object to or restrict processing, and to opt out of the sale or sharing of personal information for targeted advertising. To exercise these rights, use our <a href="contact.html">contact form</a> and choose "Privacy request". You may also complain to your local data-protection authority.</p>
<h2>8. Retention and security</h2><p>We keep information only as long as needed for the purposes above or as required by law, and use reasonable safeguards. No method of transmission over the Internet is completely secure.</p>
<h2>9. Children</h2><p>The Site is not directed to children under 13 (or 16 in some regions), and we do not knowingly collect their information.</p>
<h2>10. Changes</h2><p>We may update this policy and will change the date above when we do.</p>
<h2>11. Contact</h2><p>Questions? Use our <a href="contact.html">contact form</a>.</p>"""

def terms_body():
    return """
<p>By using Smart.Legal you agree to these Terms. If you do not agree, please do not use the Site.</p>
<h2>1. Information only — no legal advice</h2><p>Content, tools, templates and calculators are general information and are not legal advice. Smart.Legal is not a law firm and is not a lawyer referral service. No attorney-client relationship is formed by using the Site or submitting a form.</p>
<h2>2. Independent attorneys and partners</h2><p>Attorneys or legal-service providers who contact you after a case review are independent. They may pay to advertise or to receive inquiries. We do not endorse, recommend or guarantee any provider, and you are responsible for checking their licence and deciding whether to hire them.</p>
<h2>3. Your use</h2><p>You agree to provide accurate information, not to misuse forms, not to submit unlawful or infringing content, and not to scrape, overload or interfere with the Site.</p>
<h2>4. Templates and tools</h2><p>Templates and calculators are provided "as is" without warranty of fitness for any purpose. You are responsible for adapting documents to your situation and jurisdiction.</p>
<h2>5. Third-party content</h2><p>News headlines, videos and external links are provided for convenience; we are not responsible for third-party content.</p>
<h2>6. Donations, contests and sponsorships</h2><p>Donations are voluntary and non-refundable once processed unless required by law. Contests are governed by the rules on the Contests page. Sponsored content is labelled.</p>
<h2>7. Intellectual property</h2><p>Site content, design and code are owned by Smart.Legal or its licensors. You may print or share pages for personal, non-commercial use with attribution. Documents you generate with our templates are yours to use.</p>
<h2>8. Limitation of liability</h2><p>To the fullest extent permitted by law, Smart.Legal is not liable for any indirect, incidental or consequential damages, or for any loss arising from reliance on Site content. Our total liability is limited to the amount you paid us, if any, in the past 12 months.</p>
<h2>9. Changes and governing law</h2><p>We may update these Terms at any time. Continued use means acceptance. These Terms are governed by the laws applicable at the operator's principal place of business, without regard to conflict-of-law rules.</p>"""

def disclaimer_body():
    return """
<p><strong>Smart.Legal provides legal information, not legal advice.</strong></p>
<p>The guides, dictionary, news, videos, Navigator, document templates and calculators on this Site are for general educational purposes. Laws differ between countries, states, provinces and cities, and they change frequently. Information on this Site may not reflect the most current legal developments and may not apply to your situation.</p>
<p>Smart.Legal is not a law firm, does not employ attorneys to give advice to visitors and is not a lawyer referral service. Using the Site, submitting a form or communicating with us does not create an attorney-client relationship, and communications with us are not protected by attorney-client privilege.</p>
<p>Attorneys and legal-service providers who may contact you are independent third parties and may have paid to advertise on or receive inquiries through Smart.Legal. Smart.Legal does not recommend or vouch for any particular provider. Always verify a lawyer's licence with the relevant bar or law society.</p>
<p>Outcomes shown by calculators are illustrative estimates. Prior results do not guarantee similar outcomes.</p>
<p>Do not delay seeking legal advice, disregard legal advice or start or stop any legal action because of something you read on this Site. In an emergency, contact local emergency services. If you have a deadline, contact a licensed lawyer or legal-aid organisation immediately.</p>"""

def trademark_body():
    return """
<h2>Non-affiliation</h2><p>Smart.Legal is an independent website operating on the domain name smart.legal. The words "smart" and "legal" are used in their ordinary, descriptive meaning. Smart.Legal is <strong>not affiliated with, endorsed by, sponsored by or connected to</strong> any company, law firm, software product, trademark owner or service that uses "SmartLegal", "Smart Legal" or any similar name or mark, in any country. Any such names are the property of their respective owners.</p>
<h2>Third-party marks</h2><p>All other trademarks, service marks, product names and logos referenced on this Site — including those of publishers, YouTube channels, government bodies and legal-aid organisations — belong to their respective owners and are used only to identify those sources. Their use does not imply endorsement.</p>
<h2>Copyright</h2><p>&copy; Smart.Legal. All original text, guides, definitions, templates, calculators, code and design on this Site are protected by copyright. Statutes, regulations and court decisions referred to are public-domain material where applicable. News headlines are short factual references linking to the original publishers. Embedded videos remain the property of their creators and are displayed using YouTube's embedding features.</p>
<h2>Copyright complaints</h2><p>If you believe content on this Site infringes your copyright or trademark, send a notice through our <a href="contact.html">contact form</a> identifying the work, the material and its location on the Site, your contact details, and a statement of good-faith belief and accuracy. We will review and respond promptly, including removing material where appropriate.</p>"""
