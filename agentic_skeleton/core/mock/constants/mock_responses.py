"""
Mock Responses Constants
======================

Contains predefined response templates for different task categories.
Used by the mock response generator.
"""

# ----------------------------------------
#  MOCK RESPONSES
# ----------------------------------------
MOCK_RESPONSES = {
    "research": [
        "[MOCK] Research complete: Found 7 recent sources on {topic} (2024-2025). Key insights: 42% increase in enterprise adoption since Q1 2024, 3 emerging applications in healthcare (telemedicine, remote monitoring, predictive diagnostics), and integration with quantum computing starting Q3 2025.",
        "[MOCK] Completed research on {topic}. Analysis of 12 academic papers shows consensus on core principles (87% agreement) but significant divergence in implementation approaches (4 competing methodologies). Latest 2025 paper suggests hybrid approach combining methods A and C.",
        "[MOCK] Research findings on {topic}: Market size reached $3.8B in Q1 2025 (27% YoY growth), projected to reach $6.2B by 2027. Identified 3 enterprise solutions (market leaders) and 5 promising open-source alternatives with active development communities."
    ],
    "write": [
        "[MOCK] Draft completed for {topic}. The 850-word document covers healthcare applications of machine learning, patient data analysis, medical diagnostics, and treatment optimization. Historical context (2010-2023), current applications (2024-2025), and future trends (2026+). Includes 5 key points with supporting examples and 8 expert quotes from hospital administrators.",
        "[MOCK] Created a comprehensive overview of {topic} (1,200 words). Introduction establishes healthcare impact ($4.2B market by 2026), three main sections explore medical diagnostics, patient care, and hospital management with machine learning algorithms, with conclusion highlighting implementation roadmap for 2025-2026.",
        "[MOCK] Written content on {topic} now ready for review (950 words). Structured in problem-solution format with balanced perspective on healthcare advantages (7 identified benefits) and limitations (4 current challenges). Includes case studies from leading medical organizations implementing machine learning in 2025."
    ],
    "analyze": [
        "[MOCK] Analysis shows {topic} has 3 distinct patterns: increasing artificial intelligence adoption (42% YoY in 2025), shifting job market demographics (technical professionals +23%, automation replacing manual jobs +15%), and evolving workforce needs (AI programming +40%, algorithm development +68%, traditional jobs -12%).",
        "[MOCK] Completed comparative analysis of {topic} impact on employment. AI automation outperforms in speed (32% faster) and resource usage (18% lower), changing the workforce landscape. Analysis shows job creation in AI sectors offsetting losses in manual labor. ROI analysis shows AI jobs superior for economic growth.",
        "[MOCK] Trend analysis for {topic}: Identified cyclical pattern in AI and job markets with 6-month periodicity. Artificial intelligence is transforming employment patterns with peak disruption in Q2 and Q4 (32% and 28% above baseline). Three workforce anomalies detected in 2024-2025 data, correlating with AI market disruptions. Recommend quarterly workforce review cycle with automated anomaly detection."
    ],
    "develop": [
        "[MOCK] Implemented core functionality for {topic}. Created REST API for a bookstore application with 6 microservices with clean domain boundaries, 87% test coverage (unit + integration), and automated CI/CD pipeline. Book inventory database model and store CRUD operations implemented. Performance benchmarks show 250ms average response time under simulated load of 1000 concurrent users.",
        "[MOCK] Development complete for {topic}. Built RESTful API endpoints for bookstore inventory management with database model for books, authors, and store locations. Implemented CRUD operations for book catalog with HTTP GET/POST/PUT/DELETE endpoints. Architectural documentation includes entity-relationship diagrams and API specification (OpenAPI 3.0).",
        "[MOCK] Finished developing {topic} architecture. Created API server with 12 endpoints for bookstore management (inventory, customers, orders). Database schema optimized for book metadata queries and store operations. Implemented JWT authentication, input validation, and error handling. REST API response times averaging <100ms (p95) for typical book catalog operations."
    ],
    "design": [
        "[MOCK] Created wireframes for {topic} interface. Includes 8 key screens with responsive layouts for desktop, tablet, and mobile. Accessibility review complete (WCAG 2.2 AAA compliance) with dark mode support and voice navigation integration.",
        "[MOCK] Completed user flow diagrams for {topic}. Optimized task completion from 12 steps to 5 steps for core journeys. Added personalization pathways based on user behavior and accessibility preferences. Compliance with 2025 EU Digital Services Act verified.",
        "[MOCK] Design system for {topic} now ready with 42 reusable components, neural-adaptive color system, typography optimized for 8 languages, and motion design principles supporting spatial computing environments. Component library published with Figma and code integration."
    ],
    "data-science": [
        "[MOCK] Data preprocessing complete for {topic}: Cleaned 32,450 records (removed duplicates, handled missing values), feature engineering added 8 derived variables, and dimensional reduction applied using PCA maintaining 92% variance with 6 components.",
        "[MOCK] Model evaluation results for {topic}: Ensemble approach outperformed baseline by 37%. Final model combines gradient boosting (65% weight) and transformer architecture (35% weight) with F1-score of 0.92 and latency under 100ms on standard hardware.",
        "[MOCK] Deployed {topic} prediction pipeline with real-time inferencing capability (handling 2,000 req/sec). Implementation includes bias monitoring dashboard, data drift detection with automated alerts, and A/B testing framework for continuous improvement."
    ],
    "default": [
        "[MOCK] Completed the requested task for {topic}. Results ready for review and next steps. Documentation included with implementation details and recommendations for future enhancements.",
        "[MOCK] Task finished successfully. The {topic} has been processed according to specifications with all acceptance criteria met. Performance metrics show 35% improvement over baseline.",
        "[MOCK] Completed work on {topic}. Deliverables include comprehensive documentation, implementation code, and validation tests. Security audit passed with zero critical findings."
    ],
    "job_market": [
        "[MOCK] Analysis of {topic} job market trends complete. Identified 5 high-growth roles (ML engineers +42%, AI ethicists +65%, prompt engineers +120%) and 3 declining roles. Salary ranges $120K-$250K with highest demand in healthcare, finance, and autonomous systems. Remote work options available for 72% of positions.",
        "[MOCK] Job market analysis for {topic} and machine learning sectors finished. Machine learning engineers are in highest demand (38% YoY growth), followed by AI product managers and MLOps specialists. Top skills required: PyTorch/TensorFlow (95% of listings), cloud deployment (87%), and prompt engineering (76%).",
        "[MOCK] {topic} employment landscape report ready: 12,000+ open positions across Fortune 500 companies, 37% requiring advanced degrees. Top hiring regions: US West Coast, NYC metro, and emerging hubs in Austin and Toronto. Machine learning specialists commanding 28% premium over standard software roles."
    ],
    "bookstore": [
        "[MOCK] {topic} application development completed with inventory management (10,000+ titles), customer account system, and recommendation engine. Features include real-time inventory tracking, secure payment processing (PCI-DSS compliant), and personalized recommendations based on purchase history.",
        "[MOCK] {topic} platform implemented with three core modules: inventory management, customer relations, and sales analytics. System handles 5,000+ concurrent users with 99.9% uptime and includes mobile-responsive design with full feature parity across devices.",
        "[MOCK] Online {topic} application ready for deployment with complete order management workflow, inventory system tracking 15,000+ titles, and customer loyalty program. Integration with major payment processors and shipping APIs allows for seamless checkout experience."
    ]
}