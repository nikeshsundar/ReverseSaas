export type TechnologySignal = {
  name: string;
  confidence: number;
};

export type TechnologyStackData = {
  frontend: TechnologySignal[];
  backend: TechnologySignal[];
  database: TechnologySignal[];
  hosting: TechnologySignal[];
  analytics: TechnologySignal[];
  payments: TechnologySignal[];
};

export type FeatureItem = {
  title: string;
  description: string;
};

export type CompetitorItem = {
  name: string;
  description: string;
};

export type CostBreakdown = {
  hosting: number;
  database: number;
  storage: number;
  bandwidth: number;
  total: number;
};

export type CostEstimateData = {
  users_100: CostBreakdown;
  users_1000: CostBreakdown;
  users_10000: CostBreakdown;
  users_100000: CostBreakdown;
};

export type ArchitectureNode = {
  id: string;
  label: string;
  category: string;
  x: number;
  y: number;
};

export type ArchitectureEdge = {
  id: string;
  source: string;
  target: string;
};

export type ArchitectureGraphData = {
  nodes: ArchitectureNode[];
  edges: ArchitectureEdge[];
};

export type AIInsights = {
  startup_summary: string;
  target_customers: string;
  problem_solved: string;
  core_features: string[];
  business_model: string;
  revenue_strategy: string;
  competitive_advantages: string[];
  weaknesses: string[];
  market_category: string;
  roadmap: string[];
};

export type AnalysisResponse = {
  id: string;
  url: string;
  company_name: string | null;
  description: string | null;
  industry: string | null;
  created_at: string;
  status: "pending" | "processing" | "completed" | "failed";
  error?: string | null;
  ai_insights?: AIInsights | null;
  architecture?: ArchitectureGraphData | null;
  features: FeatureItem[];
  competitors: CompetitorItem[];
  cost_estimate?: CostEstimateData | null;
  technology_stack?: TechnologyStackData | null;
  metadata?: Record<string, unknown> | null;
};
