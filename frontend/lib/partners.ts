export interface PartnerProgram {
  slug: string;
  name: string;
  platform: 'PartnerStack' | 'Impact' | 'Impact.com';
  category: string;
  description: string;
  excerpt: string;
  keywords: string[];
  url: string;
  logo: string;
  cta: string;
  featured?: boolean;
}

export const partnerPrograms: PartnerProgram[] = [
  // PartnerStack programs
  {
    slug: 'clickup',
    name: 'ClickUp',
    platform: 'PartnerStack',
    category: 'Project Management',
    description: 'ClickUp is an all-in-one productivity platform that helps teams manage projects, tasks, and collaboration. It offers Gantt charts, Kanban boards, time tracking, and custom views that help federal contractors stay on top of complex compliance timelines.',
    excerpt: 'All-in-one project management platform ideal for federal contractors managing complex compliance and delivery timelines.',
    keywords: ['project management', 'task tracking', 'federal contractors', 'compliance timelines', 'collaboration'],
    url: 'https://partnerstack.com/go/clickup',
    logo: '/partners/clickup.svg',
    cta: 'Explore ClickUp',
    featured: true,
  },
  {
    slug: 'gusto',
    name: 'Gusto',
    platform: 'PartnerStack',
    category: 'HR & Payroll',
    description: 'Gusto simplifies payroll, benefits, and HR compliance for businesses. Their platform handles federal tax deposits, workers comp, and compliance reporting — critical for government contractors managing subcontractor and employee requirements.',
    excerpt: 'Payroll, benefits, and HR compliance platform built for growing businesses and government contractors.',
    keywords: ['payroll', 'HR compliance', 'federal tax', 'benefits', 'government contractors'],
    url: 'https://partnerstack.com/go/gusto',
    logo: '/partners/gusto.svg',
    cta: 'Explore Gusto',
  },
  {
    slug: 'onelogin',
    name: 'OneLogin',
    platform: 'PartnerStack',
    category: 'Cybersecurity',
    description: 'OneLogin provides cloud-based identity and access management that helps organizations secure digital assets. Their SSO and MFA solutions align well with FedRAMP and NIST 800-53 compliance requirements.',
    excerpt: 'Cloud identity and access management platform supporting FedRAMP and NIST compliance.',
    keywords: ['identity management', 'SSO', 'MFA', 'FedRAMP', 'NIST 800-53', 'cybersecurity'],
    url: 'https://partnerstack.com/go/onelogin',
    logo: '/partners/onelogin.svg',
    cta: 'Explore OneLogin',
  },
  {
    slug: 'slack',
    name: 'Slack',
    platform: 'PartnerStack',
    category: 'Communication',
    description: 'Slack is a team communication platform that brings all conversations, files, and tools together. Its integration ecosystem makes it ideal for federal teams coordinating across secure environments.',
    excerpt: 'Team communication platform with deep integrations for federal collaborative workflows.',
    keywords: ['communication', 'collaboration', 'federal teams', 'integrations', 'workflow'],
    url: 'https://partnerstack.com/go/slack',
    logo: '/partners/slack.svg',
    cta: 'Explore Slack',
  },
  {
    slug: 'hubspot',
    name: 'HubSpot',
    platform: 'PartnerStack',
    category: 'Marketing',
    description: 'HubSpot offers an integrated CRM, marketing automation, sales pipeline, and customer service platform. Government agencies increasingly use HubSpot for constituent engagement and campaign management.',
    excerpt: 'Integrated CRM and marketing platform for government constituent engagement.',
    keywords: ['CRM', 'marketing automation', 'government engagement', 'sales pipeline'],
    url: 'https://partnerstack.com/go/hubspot',
    logo: '/partners/hubspot.svg',
    cta: 'Explore HubSpot',
    featured: true,
  },
  // Impact.com programs
  {
    slug: 'shopify',
    name: 'Shopify',
    platform: 'Impact',
    category: 'E-Commerce',
    description: 'Shopify powers e-commerce for millions of businesses worldwide. Its platform supports secure payment processing, inventory management, and multi-channel sales — key capabilities for government procurement portals.',
    excerpt: 'E-commerce platform powering secure online storefronts and procurement.',
    keywords: ['e-commerce', 'online storefront', 'procurement', 'payment processing'],
    url: 'https://impact.com/shopify',
    logo: '/partners/shopify.svg',
    cta: 'Explore Shopify',
  },
  {
    slug: 'segment',
    name: 'Segment (Twilio)',
    platform: 'Impact',
    category: 'Analytics',
    description: 'Segment is a customer data platform by Twilio that collects, cleans, and routes customer data in real-time. Government agencies use it to build unified views of constituent interactions across channels.',
    excerpt: 'Customer data platform enabling unified analytics across government channels.',
    keywords: ['analytics', 'customer data', 'twilio', 'unified view', 'government channels'],
    url: 'https://impact.com/segment',
    logo: '/partners/segment.svg',
    cta: 'Explore Segment',
  },
  {
    slug: 'mailchimp',
    name: 'Mailchimp',
    platform: 'Impact',
    category: 'Marketing',
    description: 'Mailchimp provides email marketing automation, audience segmentation, and campaign analytics. It helps organizations maintain compliant communication with stakeholders and constituents.',
    excerpt: 'Email marketing automation and audience segmentation for government communications.',
    keywords: ['email marketing', 'automation', 'segmentation', 'government communications'],
    url: 'https://impact.com/mailchimp',
    logo: '/partners/mailchimp.svg',
    cta: 'Explore Mailchimp',
  },
  {
    slug: 'adobe-experience-manager',
    name: 'Adobe Experience Manager',
    platform: 'Impact',
    category: 'Content Management',
    description: 'AEM provides enterprise-grade content management and digital experience capabilities. It is widely adopted by federal agencies for secure, scalable government websites and digital services.',
    excerpt: 'Enterprise content management platform trusted by federal agencies worldwide.',
    keywords: ['content management', 'digital experience', 'federal websites', 'enterprise'],
    url: 'https://impact.com/adobe-aem',
    logo: '/partners/adobe.svg',
    cta: 'Explore AEM',
  },
  {
    slug: 'stripe',
    name: 'Stripe',
    platform: 'Impact',
    category: 'Payments',
    description: 'Stripe offers a comprehensive payment processing platform supporting diverse payment methods. Government agencies leverage Stripe for online payment collection and subscription-based services.',
    excerpt: 'Payment processing platform with compliance features for government collection.',
    keywords: ['payments', 'payment processing', 'government collection', 'compliance'],
    url: 'https://impact.com/stripe',
    logo: '/partners/stripe.svg',
    cta: 'Explore Stripe',
    featured: true,
  },
];

export function getAllPartners(): PartnerProgram[] {
  return partnerPrograms.sort((a, b) => {
    if (a.featured && !b.featured) return -1;
    if (!a.featured && b.featured) return 1;
    return a.name.localeCompare(b.name);
  });
}

export function getPartnerBySlug(slug: string): PartnerProgram | undefined {
  return partnerPrograms.find(p => p.slug === slug);
}

export function getPartnersByCategory(category: string): PartnerProgram[] {
  return partnerPrograms.filter(p => p.category === category);
}

export function getPartnersByPlatform(platform: string): PartnerProgram[] {
  return partnerPrograms.filter(p => p.platform === platform);
}

export function searchPartners(query: string): PartnerProgram[] {
  const lowerQuery = query.toLowerCase();
  return partnerPrograms.filter(p =>
    p.name.toLowerCase().includes(lowerQuery) ||
    p.description.toLowerCase().includes(lowerQuery) ||
    p.keywords.some(k => k.toLowerCase().includes(lowerQuery)) ||
    p.category.toLowerCase().includes(lowerQuery)
  );
}
