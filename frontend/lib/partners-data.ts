import type { PartnerProgram } from './partners'

export const partnerProgramsData: PartnerProgram[] = [
  // PartnerStack programs
  {
    slug: 'clickup',
    name: 'ClickUp',
    platform: 'PartnerStack',
    category: 'Project Management',
    description: 'ClickUp is an all-in-one productivity platform for managing projects, tasks, and collaboration: boards, timelines, time tracking, and custom views that keep delivery visible.',
    excerpt: 'All-in-one project management platform for teams running complex delivery timelines.',
    keywords: ['project management', 'task tracking', 'collaboration', 'delivery timelines', 'boards'],
    url: 'https://try.web.clickup.com/f1xmsye5bi9s-ftpxvl',
    logo: '/partners/clickup.svg',
    cta: 'Explore ClickUp',
    featured: true,
  },
  {
    slug: 'gusto',
    name: 'Gusto',
    platform: 'PartnerStack',
    category: 'HR & Payroll',
    description: 'Gusto simplifies payroll, benefits, and HR for growing businesses: automated filings, workers comp, and reporting in one place.',
    excerpt: 'Payroll, benefits, and HR platform built for growing businesses.',
    keywords: ['payroll', 'HR', 'benefits', 'onboarding', 'small business'],
    url: 'https://get.gusto.com/703bagjmmd7u',
    logo: '/partners/gusto.svg',
    cta: 'Explore Gusto',
  },
  // Impact.com programs
];
