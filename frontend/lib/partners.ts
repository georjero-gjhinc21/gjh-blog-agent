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

import { partnerProgramsData } from './partners-data'
import { partnerProgramsGenerated } from './partners-generated'

export const partnerPrograms: PartnerProgram[] = [...partnerProgramsData, ...partnerProgramsGenerated]


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
