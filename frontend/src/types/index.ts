export enum Domains {
  benefits = 'BENEFITS',
  provider = 'PROVIDER',
  pharmacy = 'PHARMACY',
  financial = 'FINANCIAL',
  claims = 'CLAIMS',
  healthLibrary = 'HEALTH',
  unknown = 'UNKNOWN',
}

export enum Feedback {
  yes = 'Yes',
  no = 'No',
}

declare global {
  type TSearchContentVariant = 'md' | 'html';

  interface IDomainMatchPercentage {
    domain: Domains;
    percentage: number;
  }

  interface ISearchResultItem {
    title: string;
    content: string;
    variant: TSearchContentVariant;
  }

  interface ISearchResultResponse {
    title: string;
    url: string;
    skill: string;
    domain: Domains;
    content: string;
    variant: TSearchContentVariant;
    score: number;
  }

  interface ISearchResponse {
    traceId?: string;
    domains: Array<IDomainMatchPercentage>;
    query: string;
    results: Array<ISearchResultResponse>;
  }
}
