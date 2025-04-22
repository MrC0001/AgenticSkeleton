"""
Domain Knowledge Constants
========================

Contains domain-specific knowledge and response templates.
Used by the mock response generator.
"""

import random

# ----------------------------------------
#  DOMAIN KNOWLEDGE
# ----------------------------------------
DOMAIN_KNOWLEDGE = {
    "cloud_computing": {
        "keywords": ["cloud platform", "microsoft azure", "aws", "amazon web services", 
                    "google cloud", "azure", "cloud computing", "cloud infrastructure",
                    "cloud services", "cloud migration", "cloud native", "serverless", 
                    "multi-region", "cloud costs", "cloud deployment"],
        "subtasks": {
            "research": {
                "patterns": ["research", "analyze", "compare", "evaluate", "assess", "study", "investigate"],
                "template": "[MOCK] Cloud research complete: Evaluated {topic} across 3 major providers (AWS, Azure, GCP). Azure leads in enterprise integration (76% compatibility score), AWS in cost-effectiveness for variable workloads (22% lower TCO), and GCP in ML/AI capabilities (3.2x faster training time on standard benchmarks).",
                "variables": {
                    "compatibility": lambda: random.randint(65, 95),
                    "cost_reduction": lambda: random.randint(15, 40),
                    "performance": lambda: round(random.uniform(2.5, 4.5), 1)
                }
            },
            "implement": {
                "patterns": ["implement", "deploy", "build", "create", "construct", "develop", "integrate"],
                "template": "[MOCK] Successfully deployed {topic} as multi-region cloud solution with 99.99% availability SLA. Architecture includes auto-scaling compute (handling 10,000+ concurrent users), geo-redundant storage with 11ms average access time, and zero-trust security model (SOC2/ISO27001 compliant).",
                "variables": {
                    "availability": lambda: "99.99%" if random.random() > 0.5 else "99.999%",
                    "users": lambda: f"{random.randint(5, 50)}k",
                    "latency": lambda: random.randint(8, 25)
                }
            },
            "optimize": {
                "patterns": ["optimize", "improve", "enhance", "refine", "streamline", "tune", "refactor", "costs"],
                "template": "[MOCK] Cloud optimization complete for {topic}: Reduced monthly costs by 38% ($47,500 annualized savings), decreased cold start latency by 64% (now 230ms avg), and implemented FinOps dashboard with proactive cost anomaly detection. Reserved instances now cover 85% of predictable workloads.",
                "variables": {
                    "cost_reduction": lambda: random.randint(25, 45),
                    "savings": lambda: f"${random.randint(30, 75)},{random.choice(['000', '500'])}",
                    "latency_improvement": lambda: random.randint(40, 70)
                }
            }
        }
    },
    "ai_ml": {
        "keywords": ["artificial intelligence", "machine learning", "neural network", "deep learning", 
                  "nlp", "natural language processing", "computer vision", "predictive model", 
                  "data science", "ai model", "ml pipeline", "generative ai", "large language model", "ai"],
        "subtasks": {
            "research": {
                "patterns": ["research", "analyze", "compare", "evaluate", "assess", "study", "investigate", "impact"],
                "template": "[MOCK] AI/ML research on {topic} complete: Benchmarked 5 algorithms against current SOTA models. New approach achieves 93.2% accuracy (+7.8% over baseline) while reducing parameter count by 62% (678M vs 1.8B) and inference time by 43% (enabling real-time applications).",
                "variables": {
                    "accuracy": lambda: round(random.uniform(88.5, 96.8), 1),
                    "parameter_reduction": lambda: random.randint(35, 75),
                    "models_tested": lambda: random.randint(4, 8)
                }
            },
            "data": {
                "patterns": ["data", "collect", "preprocess", "clean", "prepare", "gather", "dataset"],
                "template": "[MOCK] Prepared dataset for {topic}: Processed 2.8M samples with automated cleaning pipeline (98.7% accuracy verified with manual review). Created balanced training/validation/test splits (70/15/15) with stratification across 7 key variables. Data augmentation increased effective samples by 3.5x for minority classes.",
                "variables": {
                    "samples": lambda: f"{random.randint(1, 10)}.{random.randint(1, 9)}M",
                    "accuracy": lambda: round(random.uniform(97.5, 99.8), 1),
                    "variables": lambda: random.randint(5, 12)
                }
            },
            "model": {
                "patterns": ["model", "train", "develop", "build", "create", "implement", "design"],
                "template": "[MOCK] Developed {topic} model with ensemble architecture: Transformer backbone (1.2B parameters) with domain-specific adapters reducing computational requirements by 78%. Achieved SOTA results on 3 benchmarks (F1: 0.94, BLEU: 42.5, ROUGE-L: 0.89) with 240ms average inference time.",
                "variables": {
                    "params": lambda: f"{random.randint(1, 3)}.{random.randint(1, 9)}B",
                    "efficiency": lambda: random.randint(65, 85),
                    "benchmarks": lambda: random.randint(2, 5)
                }
            },
            "deploy": {
                "patterns": ["deploy", "implement", "integrate", "release", "publish", "operationalize", "serve"],
                "template": "[MOCK] Deployed {topic} system to production: REST API handles 1,800 req/sec with auto-scaling (p99 latency: 485ms). Implemented A/B testing framework, monitoring for concept drift (7-day sliding window), and explainability module for regulatory compliance. Full CI/CD with daily fine-tuning.",
                "variables": {
                    "throughput": lambda: random.randint(800, 3000),
                    "latency": lambda: random.randint(250, 750),
                    "window": lambda: random.choice([7, 14, 30])
                }
            }
        }
    },
    "healthcare_tech": {
        "keywords": ["healthcare", "medical", "health informatics", "clinical", "patient care", 
                  "telehealth", "health monitoring", "medical imaging", "healthcare ai", 
                  "medical technology", "health records", "ehr", "remote patient monitoring",
                  "patient outcomes", "medical diagnosis"],
        "subtasks": {
            "research": {
                "patterns": ["research", "analyze", "investigate", "evaluate", "assess", "study", "review", "impact"],
                "template": "[MOCK] Healthcare research complete for {topic}: Analyzed 12 clinical studies (7,850 total patients) across major healthcare systems. Solution demonstrates 28% reduction in readmission rates, 42% improvement in early diagnosis accuracy, and 17% decrease in treatment costs. All findings HIPAA and GDPR compliant.",
                "variables": {
                    "studies": lambda: random.randint(8, 15),
                    "patients": lambda: f"{random.randint(5, 12)},{random.randint(100, 999)}",
                    "improvement": lambda: random.randint(25, 50)
                }
            },
            "design": {
                "patterns": ["design", "architect", "plan", "blueprint", "outline", "framework", "structure"],
                "template": "[MOCK] Designed {topic} for healthcare environment with dual focus on clinical workflow integration and regulatory compliance. Solution includes role-based access control (14 permission levels), real-time PHI anonymization (meeting HIPAA Safe Harbor), and integration with 8 major EHR systems (including Epic, Cerner).",
                "variables": {
                    "roles": lambda: random.randint(8, 16),
                    "compliance": lambda: random.choice(["HIPAA + GDPR", "HIPAA + HITECH", "HIPAA Safe Harbor", "ISO 13485"]),
                    "systems": lambda: random.randint(5, 10)
                }
            },
            "implement": {
                "patterns": ["implement", "develop", "build", "create", "construct", "deploy", "integrate"],
                "template": "[MOCK] Implemented {topic} system with secure medical data pipeline (zero PHI exposure) and clinical decision support module. Deployment completed across 3 hospital networks (42 locations) with 98.7% staff adoption. System processes 12,450 patient records daily with 350ms average response time.",
                "variables": {
                    "locations": lambda: random.randint(25, 60),
                    "adoption": lambda: round(random.uniform(94.5, 99.5), 1),
                    "records": lambda: f"{random.randint(8, 15)},{random.randint(100, 999)}"
                }
            },
            "evaluate": {
                "patterns": ["evaluate", "assess", "measure", "analyze", "test", "validate", "verify"],
                "template": "[MOCK] Evaluated {topic} through clinical validation study (IRB approved) with 1,240 patients across 5 care environments. Results show 32% improvement in primary clinical outcome measures, 94.7% provider satisfaction score, and $3.8M annualized cost savings in pilot deployment group.",
                "variables": {
                    "patients": lambda: f"{random.randint(1, 2)},{random.randint(100, 999)}",
                    "improvement": lambda: random.randint(25, 40),
                    "satisfaction": lambda: round(random.uniform(88.5, 96.5), 1)
                }
            }
        }
    }
}