export interface IPaper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  cluster: number;
  year: number;
  references: string[];
  citations: number;
  is_influential: boolean;
}
