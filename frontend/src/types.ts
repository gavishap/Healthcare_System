export interface Evidence { id:string; citation_id:string; locator:string; text:string; content_hash:string }
export interface Citation {
  id:string; rank:number; source:string; canonical_id:string; url:string; title:string;
  published_date:string|null; updated_date:string|null; retrieved_at:string; evidence_class:string;
  decision:string; reason_codes:string[]; allowed_claim_types:string[]; access_level:string;
  family_id:string; family_basis:string; family_count:number; duplicate_of:string|null; snapshot_hash:string;
  is_synthetic?:boolean;
  display_bucket?:string; eligible_sections?:string[]; population_tags?:string[];
  population?:{conditions?:string[];tags?:string[];minimum_age?:string;maximum_age?:string;sex?:string;countries?:string[];eligibility_criteria?:string};
  evidence:Evidence[]; phase:string|null; status:string|null; has_results:boolean;
  relevance_terms_matched:number; relevance_terms_total:number; authors:string[]; journal:string|null;
  organization_roles:{name:string;role:string;study_id:string;locator:string;organization_class?:string}[];
}
export interface Reference { evidence_id:string; citation_id:string; quote:string; locator:string; snapshot_hash:string }
export interface Claim { id:string; section:string; claim_type:string; text:string; references:Reference[]; origin:string; support_check:string; review_needed:boolean; support_explanation?:string }
export interface Conflict { id:string; claim_ids:string[]; citation_ids:string[]; type:string; summary:string; resolution:string; status:string }
export interface Result {
  scope?:{raw_condition:string;condition:string;population:string[];jurisdiction:string};
  condition:string; mode:string; status:string; as_of:string; policy_version:string; citations:Citation[]; claims:Claim[];
  excluded_claims:{text:string;reason_codes:string[];explanation?:string}[]; conflicts:Conflict[]; warnings:string[];
  coverage:Record<string,{status:string;reason:string}>; ranking_explanation:string;
  source_attempts:{source:string;status:string;retrieved?:number;reason?:string;truncated?:boolean}[];
  usage:{model_requests:number;requests:{stage:string;input_tokens:number;output_tokens:number}[];tool_calls:{name:string;status:string;evidence_count:number}[];cost_usd:null}; model:string|null;
}
export interface Run {id:string;condition:string;status:string;mode:string;created_at:string;finished_at?:string;result:Result|null;events:{stage:string;message:string;created_at:string}[]}
export interface RunSummary {id:string;condition:string;status:string;mode:string;created_at:string}
export interface Policy {version:string;criteria:{criterion:string;rule:string}[];source_registry:{id:string;host:string;role:string}[];conflict_rule:string;scope:string;model:string;model_configured:boolean;ncbi_key_configured:boolean}
