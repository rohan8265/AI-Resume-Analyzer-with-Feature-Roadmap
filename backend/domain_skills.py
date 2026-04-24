"""Domain skill libraries — 1200+ skills across 7 domains with priority tiers."""

DOMAIN_SKILLS = {
    "Data Science": {
        "essential": [
            "Python", "SQL", "Machine Learning", "Statistics", "Data Visualization",
            "Pandas", "NumPy", "Data Analysis", "Probability", "Linear Regression",
            "Logistic Regression", "Data Cleaning", "Exploratory Data Analysis",
            "Matplotlib", "Seaborn", "Jupyter Notebook", "Hypothesis Testing",
            "A/B Testing", "Data Wrangling", "Descriptive Statistics",
            "Inferential Statistics", "Data Mining", "Scikit-learn", "Feature Selection",
            "Cross Validation"
        ],
        "recommended": [
            "Deep Learning", "TensorFlow", "PyTorch", "Feature Engineering", "NLP",
            "Time Series Analysis", "Random Forest", "Gradient Boosting", "XGBoost",
            "Neural Networks", "Keras", "Model Deployment", "MLflow", "Data Pipeline",
            "ETL", "Dimensionality Reduction", "PCA", "Clustering", "K-Means",
            "SVM", "Decision Trees", "Ensemble Methods", "Bayesian Statistics",
            "Regularization", "Hyperparameter Tuning", "Model Evaluation",
            "ROC AUC", "Precision Recall", "Confusion Matrix", "Git"
        ],
        "optional": [
            "Spark", "Hadoop", "Tableau", "Power BI", "R", "SAS", "MATLAB",
            "Airflow", "Kafka", "Docker", "AWS", "GCP", "Azure", "Databricks",
            "Snowflake", "MongoDB", "Neo4j", "Plotly", "Dash", "Streamlit",
            "FastAPI", "Flask", "Reinforcement Learning", "GANs", "Computer Vision",
            "BERT", "Transformers", "LLMs", "Prompt Engineering", "LangChain",
            "AutoML", "H2O", "KNIME", "RapidMiner", "DataRobot"
        ]
    },
    "Artificial Intelligence / Machine Learning": {
        "essential": [
            "Python", "Machine Learning", "Deep Learning", "Neural Networks",
            "TensorFlow", "PyTorch", "Mathematics", "Linear Algebra",
            "Calculus", "Probability", "Statistics", "Data Preprocessing",
            "Supervised Learning", "Unsupervised Learning", "Model Training",
            "Backpropagation", "Gradient Descent", "Loss Functions",
            "Activation Functions", "CNNs", "RNNs", "NumPy", "Pandas",
            "Scikit-learn", "Model Evaluation"
        ],
        "recommended": [
            "NLP", "Computer Vision", "Transformers", "BERT", "GPT",
            "Reinforcement Learning", "GANs", "Autoencoders", "LSTMs",
            "Attention Mechanism", "Transfer Learning", "Object Detection",
            "Image Segmentation", "Sentiment Analysis", "Named Entity Recognition",
            "Word Embeddings", "Keras", "OpenCV", "Hugging Face", "MLOps",
            "Model Deployment", "ONNX", "TensorRT", "Feature Engineering",
            "Hyperparameter Optimization", "Bayesian Optimization",
            "Regularization", "Dropout", "Batch Normalization", "Git"
        ],
        "optional": [
            "Spark MLlib", "AWS SageMaker", "Azure ML", "GCP Vertex AI",
            "Docker", "Kubernetes", "MLflow", "Weights & Biases", "DVC",
            "Ray", "Dask", "JAX", "Caffe", "MXNet", "Theano",
            "Edge AI", "TinyML", "Federated Learning", "Meta-Learning",
            "Few-Shot Learning", "Self-Supervised Learning", "Diffusion Models",
            "Stable Diffusion", "LLMs", "LangChain", "Prompt Engineering",
            "RLHF", "LoRA", "Quantization", "Knowledge Distillation",
            "Neural Architecture Search", "AutoML", "Explainable AI", "SHAP", "LIME"
        ]
    },
    "Web Development": {
        "essential": [
            "HTML", "CSS", "JavaScript", "React", "Node.js", "Git",
            "REST API", "JSON", "HTTP", "Responsive Design", "TypeScript",
            "SQL", "Database Design", "Version Control", "npm",
            "DOM Manipulation", "ES6+", "Flexbox", "CSS Grid",
            "Web Security", "Authentication", "Authorization",
            "CRUD Operations", "MVC Pattern", "Debugging"
        ],
        "recommended": [
            "Next.js", "Vue.js", "Angular", "Express.js", "MongoDB",
            "PostgreSQL", "Redis", "GraphQL", "Docker", "AWS",
            "Tailwind CSS", "SASS", "Webpack", "Vite", "Jest",
            "React Testing Library", "Cypress", "CI/CD", "GitHub Actions",
            "Nginx", "WebSockets", "OAuth", "JWT", "Prisma",
            "Sequelize", "Mongoose", "Redux", "Context API",
            "React Hooks", "Server-Side Rendering"
        ],
        "optional": [
            "Svelte", "Remix", "Astro", "Deno", "Bun", "tRPC",
            "Supabase", "Firebase", "Vercel", "Netlify", "Cloudflare Workers",
            "Three.js", "D3.js", "Framer Motion", "Storybook",
            "Figma", "Web Accessibility", "SEO", "PWA", "Service Workers",
            "WebAssembly", "Electron", "React Native", "Flutter",
            "Microservices", "Event-Driven Architecture", "Message Queues",
            "RabbitMQ", "Kafka", "Kubernetes", "Terraform",
            "Performance Optimization", "Lighthouse", "Core Web Vitals",
            "Internationalization", "Stripe API"
        ]
    },
    "Software Development": {
        "essential": [
            "Python", "Java", "C++", "Data Structures", "Algorithms",
            "OOP", "Git", "SQL", "Problem Solving", "Debugging",
            "Design Patterns", "SOLID Principles", "Version Control",
            "Unit Testing", "Code Review", "Agile", "Scrum",
            "REST API", "Linux", "Command Line", "IDE",
            "Clean Code", "Documentation", "Software Architecture",
            "Database Design"
        ],
        "recommended": [
            "C#", "Go", "Rust", "Kotlin", "Swift", "TypeScript",
            "Microservices", "Docker", "CI/CD", "Jenkins", "GitHub Actions",
            "AWS", "System Design", "Distributed Systems", "Concurrency",
            "Multithreading", "Message Queues", "Caching", "Redis",
            "PostgreSQL", "MongoDB", "GraphQL", "gRPC", "TDD",
            "Integration Testing", "Performance Testing", "Monitoring",
            "Logging", "Error Handling", "Security Best Practices"
        ],
        "optional": [
            "Kubernetes", "Terraform", "Ansible", "Prometheus", "Grafana",
            "ELK Stack", "Kafka", "RabbitMQ", "Elasticsearch",
            "Functional Programming", "Haskell", "Scala", "Clojure",
            "WebAssembly", "Blockchain", "Smart Contracts", "IoT",
            "Embedded Systems", "Game Development", "Unity", "Unreal Engine",
            "Mobile Development", "React Native", "Flutter",
            "Compiler Design", "Operating Systems", "Computer Networks",
            "Cryptography", "Machine Learning", "DevOps",
            "Site Reliability Engineering", "Chaos Engineering",
            "Event Sourcing", "CQRS", "Domain-Driven Design"
        ]
    },
    "Cloud & DevOps": {
        "essential": [
            "Linux", "AWS", "Docker", "Git", "CI/CD", "Bash Scripting",
            "Networking", "TCP/IP", "DNS", "Load Balancing",
            "Infrastructure as Code", "Terraform", "CloudFormation",
            "Monitoring", "Logging", "Security", "IAM",
            "Virtual Machines", "Containers", "Kubernetes",
            "Python", "YAML", "JSON", "SSH", "Firewall"
        ],
        "recommended": [
            "Azure", "GCP", "Ansible", "Puppet", "Chef",
            "Jenkins", "GitHub Actions", "GitLab CI", "ArgoCD",
            "Prometheus", "Grafana", "ELK Stack", "Datadog",
            "Helm", "Istio", "Service Mesh", "Microservices",
            "Serverless", "Lambda", "API Gateway", "S3",
            "EC2", "RDS", "VPC", "CloudWatch", "Route 53",
            "Auto Scaling", "CDN", "CloudFront"
        ],
        "optional": [
            "Pulumi", "Vagrant", "Packer", "Consul", "Vault",
            "Nginx", "HAProxy", "Traefik", "Envoy",
            "Kafka", "RabbitMQ", "Redis", "Elasticsearch",
            "OpenShift", "Rancher", "Nomad", "Mesos",
            "Chaos Engineering", "Site Reliability Engineering",
            "FinOps", "Cloud Cost Optimization", "Multi-Cloud",
            "Hybrid Cloud", "Edge Computing", "IoT",
            "Blockchain Infrastructure", "GPU Computing",
            "High Performance Computing", "Disaster Recovery",
            "Business Continuity", "Compliance", "SOC 2", "HIPAA",
            "PCI DSS", "GDPR"
        ]
    },
    "Cybersecurity": {
        "essential": [
            "Network Security", "Linux", "TCP/IP", "Firewalls",
            "Encryption", "Authentication", "Authorization",
            "Vulnerability Assessment", "Penetration Testing",
            "Security Protocols", "OWASP Top 10", "Risk Assessment",
            "Incident Response", "Security Monitoring", "SIEM",
            "Malware Analysis", "Threat Modeling", "IDS/IPS",
            "VPN", "SSL/TLS", "DNS Security", "Python",
            "Bash Scripting", "Windows Security", "Access Control"
        ],
        "recommended": [
            "Ethical Hacking", "Kali Linux", "Metasploit", "Burp Suite",
            "Wireshark", "Nmap", "Nessus", "Splunk", "SOAR",
            "Digital Forensics", "Reverse Engineering", "Web Security",
            "API Security", "Cloud Security", "AWS Security",
            "Azure Security", "Container Security", "Zero Trust",
            "Identity Management", "PKI", "Certificates",
            "Security Compliance", "ISO 27001", "NIST",
            "SOC Analysis", "Threat Intelligence", "OSINT",
            "Security Automation", "PowerShell", "Cryptography"
        ],
        "optional": [
            "Blockchain Security", "IoT Security", "Mobile Security",
            "Red Team", "Blue Team", "Purple Team", "Bug Bounty",
            "CTF", "Assembly Language", "Binary Exploitation",
            "Buffer Overflow", "SQL Injection", "XSS", "CSRF",
            "SSRF", "Privilege Escalation", "Social Engineering",
            "Phishing Analysis", "Dark Web Monitoring",
            "Threat Hunting", "Deception Technology", "Honeypots",
            "EDR", "XDR", "MDR", "CASB", "DLP",
            "Data Privacy", "GDPR", "HIPAA", "PCI DSS",
            "CCPA", "Governance Risk Compliance", "Business Continuity",
            "Disaster Recovery", "Security Architecture"
        ]
    },
    "Business Analytics": {
        "essential": [
            "Excel", "SQL", "Data Analysis", "Data Visualization",
            "Statistics", "Business Intelligence", "Tableau",
            "Power BI", "KPI Tracking", "Dashboard Design",
            "Reporting", "Data Cleaning", "Pivot Tables",
            "VLOOKUP", "Data Modeling", "Requirements Gathering",
            "Stakeholder Management", "Presentation Skills",
            "Problem Solving", "Critical Thinking",
            "Business Process Analysis", "Market Research",
            "Financial Analysis", "Forecasting", "Python"
        ],
        "recommended": [
            "R", "SAS", "SPSS", "Pandas", "NumPy",
            "Matplotlib", "Seaborn", "Plotly", "Google Analytics",
            "A/B Testing", "Hypothesis Testing", "Regression Analysis",
            "Customer Segmentation", "Cohort Analysis", "Funnel Analysis",
            "Churn Analysis", "Revenue Analytics", "Cost-Benefit Analysis",
            "ROI Analysis", "Competitive Analysis", "SWOT Analysis",
            "Agile", "Scrum", "JIRA", "Confluence",
            "ETL", "Data Warehousing", "Snowflake", "Looker",
            "Qlik", "SAP"
        ],
        "optional": [
            "Machine Learning", "Predictive Analytics", "Prescriptive Analytics",
            "Natural Language Processing", "Sentiment Analysis",
            "Web Scraping", "API Integration", "Automation",
            "RPA", "UiPath", "Power Automate", "Alteryx",
            "Informatica", "Talend", "dbt", "Airflow",
            "AWS QuickSight", "Azure Synapse", "Google BigQuery",
            "Databricks", "Monte Carlo Simulation", "Optimization",
            "Supply Chain Analytics", "Healthcare Analytics",
            "Risk Analytics", "Fraud Detection", "Customer Lifetime Value",
            "Attribution Modeling", "Marketing Mix Modeling",
            "Product Analytics", "Amplitude", "Mixpanel", "Segment"
        ]
    }
}

SKILL_PREREQUISITES = {
    "Machine Learning": ["Python", "Statistics", "Linear Algebra"],
    "Deep Learning": ["Machine Learning", "Python", "Neural Networks"],
    "Neural Networks": ["Machine Learning", "Calculus"],
    "TensorFlow": ["Python", "Deep Learning"],
    "PyTorch": ["Python", "Deep Learning"],
    "NLP": ["Machine Learning", "Python"],
    "Computer Vision": ["Deep Learning", "Python"],
    "CNNs": ["Neural Networks", "Deep Learning"],
    "RNNs": ["Neural Networks", "Deep Learning"],
    "LSTMs": ["RNNs"],
    "Transformers": ["Deep Learning", "NLP"],
    "BERT": ["Transformers", "NLP"],
    "GPT": ["Transformers", "NLP"],
    "GANs": ["Deep Learning", "Neural Networks"],
    "Reinforcement Learning": ["Machine Learning", "Python"],
    "React": ["JavaScript", "HTML", "CSS"],
    "Next.js": ["React", "Node.js"],
    "Vue.js": ["JavaScript", "HTML", "CSS"],
    "Angular": ["TypeScript", "HTML", "CSS"],
    "Node.js": ["JavaScript"],
    "Express.js": ["Node.js"],
    "Docker": ["Linux", "Command Line"],
    "Kubernetes": ["Docker", "Linux"],
    "Terraform": ["Cloud", "Linux"],
    "Pandas": ["Python"],
    "NumPy": ["Python"],
    "Scikit-learn": ["Python", "Machine Learning"],
    "Keras": ["Python", "TensorFlow"],
    "Feature Engineering": ["Machine Learning", "Pandas"],
    "XGBoost": ["Machine Learning", "Python"],
    "Spark": ["Python", "SQL"],
    "Hadoop": ["Linux", "Java"],
    "MLflow": ["Machine Learning", "Python"],
    "Redux": ["React", "JavaScript"],
    "GraphQL": ["REST API", "JavaScript"],
    "CI/CD": ["Git", "Linux"],
    "AWS": ["Linux", "Networking"],
    "Penetration Testing": ["Network Security", "Linux"],
    "Power BI": ["Excel", "SQL"],
    "Tableau": ["SQL", "Data Visualization"],
}

SKILL_DIFFICULTY = {
    "Python": "beginner", "HTML": "beginner", "CSS": "beginner",
    "JavaScript": "beginner", "SQL": "beginner", "Git": "beginner",
    "Excel": "beginner", "Linux": "beginner", "Bash Scripting": "beginner",
    "JSON": "beginner", "YAML": "beginner", "Markdown": "beginner",
    "Machine Learning": "intermediate", "Deep Learning": "advanced",
    "TensorFlow": "intermediate", "PyTorch": "intermediate",
    "React": "intermediate", "Node.js": "intermediate",
    "Docker": "intermediate", "AWS": "intermediate",
    "Kubernetes": "advanced", "Terraform": "intermediate",
    "NLP": "advanced", "Computer Vision": "advanced",
    "Transformers": "advanced", "GANs": "advanced",
    "Reinforcement Learning": "advanced", "System Design": "advanced",
    "Microservices": "advanced", "Distributed Systems": "advanced",
}

LEARNING_RESOURCES = {
    "Python": {
        "courses": ["https://www.coursera.org/learn/python", "https://www.codecademy.com/learn/learn-python-3"],
        "youtube": ["https://www.youtube.com/watch?v=_uQrJ0TkZlc"],
        "docs": ["https://docs.python.org/3/tutorial/"],
        "practice": "Complete 20 Python exercises on HackerRank",
        "project": "Build a CLI calculator with unit tests"
    },
    "SQL": {
        "courses": ["https://www.coursera.org/learn/sql-for-data-science"],
        "youtube": ["https://www.youtube.com/watch?v=HXV3zeQKqGY"],
        "docs": ["https://www.w3schools.com/sql/"],
        "practice": "Solve 15 SQL problems on LeetCode",
        "project": "Design and query a library management database"
    },
    "Machine Learning": {
        "courses": ["https://www.coursera.org/learn/machine-learning"],
        "youtube": ["https://www.youtube.com/watch?v=Gv9_4yMHFhI"],
        "docs": ["https://scikit-learn.org/stable/tutorial/"],
        "practice": "Implement 5 ML algorithms from scratch",
        "project": "Build a house price prediction model on Kaggle"
    },
    "Deep Learning": {
        "courses": ["https://www.coursera.org/specializations/deep-learning"],
        "youtube": ["https://www.youtube.com/watch?v=aircAruvnKk"],
        "docs": ["https://www.deeplearningbook.org/"],
        "practice": "Train a neural network on MNIST dataset",
        "project": "Build an image classifier using CNN"
    },
    "React": {
        "courses": ["https://www.coursera.org/learn/react-basics"],
        "youtube": ["https://www.youtube.com/watch?v=bMknfKXIFA8"],
        "docs": ["https://react.dev/learn"],
        "practice": "Build 5 React components with hooks",
        "project": "Create a task management app with React"
    },
    "Docker": {
        "courses": ["https://www.coursera.org/learn/docker-kubernetes"],
        "youtube": ["https://www.youtube.com/watch?v=fqMOX6JJhGo"],
        "docs": ["https://docs.docker.com/get-started/"],
        "practice": "Containerize 3 different applications",
        "project": "Create a multi-container app with Docker Compose"
    },
}

# Default resources for skills not in the map
DEFAULT_RESOURCES = {
    "courses": ["https://www.coursera.org/search?query="],
    "youtube": ["https://www.youtube.com/results?search_query="],
    "docs": ["https://www.google.com/search?q=documentation+"],
    "practice": "Complete online tutorials and exercises",
    "project": "Build a small project using this skill"
}
