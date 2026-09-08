/**
 * Canonical partner taxonomy — the ONLY category values new programs may use.
 * The classifier (utils/classify_programs.py) is constrained to this list;
 * the partners page derives filters and counts from it.
 */
export const PARTNER_CATEGORIES = [
  'Project Management',
  'HR & Payroll',
  'Cybersecurity & Identity',
  'Communication & Collaboration',
  'Marketing & CRM',
  'Finance & Accounting',
  'IT & DevOps',
  'Data & Analytics',
  'Legal & Compliance',
  'Travel & Expense',
  'Operations',
  'Other',
] as const

export type PartnerCategory = (typeof PARTNER_CATEGORIES)[number]

export const PARTNERS_PAGE_SIZE = 24
