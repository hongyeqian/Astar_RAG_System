### Meeting Purpose



- To understand the key insights that led to the fundamental shift in computing (parallel processing, GPUs).
- To explore the impact of these insights on the current AI explosion (via CUDA and AlexNet).
- To discuss the vision for what's coming next, particularly in physical AI (robotics), digital biology, and climate science.
- The interview explicitly excludes topics of company finances, management style, regulations, and politics.



### Acronyms & Orgs (Normalized)



- **NVIDIA** – Nvidia
- **CPU** – Central Processing Unit
- **GPU** – Graphics Processing Unit
- **CUDA** – Compute Unified Device Architecture
- **AI** – Artificial Intelligence
- **DGX** – Nvidia's line of AI supercomputers
- **DNNs** – Deep Neural Networks
- **TSMC** – Taiwan Semiconductor Manufacturing Company
- **OpenAI** – OpenAI



### Capability Highlights (by org)



**NVIDIA**

- Led the fundamental shift to **accelerated computing**, based on the insight that computers need both sequential (CPU) and parallel (GPU) processing.
- Initially targeted the **video games** market, which provided a large R&D budget and created a flywheel of technology and market growth.
- Views the GPU as a "time machine" that accelerates applications, allowing scientists (e.g., in quantum chemistry) to do their life's work within their lifetime.
- Created the **CUDA** platform to make parallel processing accessible to all programmers, not just graphics experts.
- Bet on deep learning after the **AlexNet** breakthrough (2012), re-engineering the entire computing stack (e.g., DGX).
- Invested tens of billions of dollars over 10 years based on the core belief in accelerated computing before the AI boom materialized.
- Core belief: Deep learning networks can scale and learn from almost any data modality (text, images, amino acids, video, robot actions).
- Developed **Omniverse** (physics simulator) and **Cosmos** (world foundation model) to train robots in realistic, physically-grounded digital worlds.
- Improved the energy efficiency of its AI computing by **10,000 times** in the 8 years since 2016.
- Maintains a core belief in **flexible, general-purpose architectures** that can support future, unknown AI algorithms, rather than over-specializing hardware for one (like Transformers).
- The GeForce RTX 50 Series graphics card uses AI to **predict most of the pixels on a screen**, computing only 500k pixels and using AI to generate the other ~7.5 million.
- Created a smaller, $3,000 "baby DGX" AI supercomputer to make AI development accessible to students and all engineers.



### Current Projects / Workstreams



- **Physical AI / Robotics**: Developing tools (Omniverse, Cosmos) to train robots, based on the belief that "everything that moves will be robotic someday".
- **Humanoid Robots**: Developing tooling and training systems; expects significant progress in the next 5 years.
- **Digital Biology**: Using AI to understand the "language of molecules" and create a "digital twin of the human".
- **Climate Science**: Applying AI to create high-resolution regional climate and weather predictions.
- **AI Energy Efficiency**: Continuing to prioritize improving the energy efficiency of AI computation.
- **Generative AI for Graphics**: Using AI to generate most of the pixels in high-end gaming graphics (AI-powered upscaling).



### Proposed Collaboration Path



- **Next 10 Years (Application Science)**: The focus of AI will shift from fundamental science to "application science" in fields like digital biology, climate tech, robotics, logistics, and teaching.
- **Human-AI Interaction**: Humans must learn to use AI to do their jobs better, just as the previous generation had to learn to use computers.
- **AI Tutors**: Recommends everyone get an AI tutor to help them learn, program, analyze, and reason, thereby empowering them and reducing the barrier to knowledge.



### Decisions



- **04:16** – NVIDIA decided at its founding to build a computer that could do both sequential processing and parallel processing.
- **05:38** – Chose video games as the first large-scale market for GPUs to fund the R&D for this new computing model.
- **08:46** – Decided to create CUDA and commit the entire company to it, believing the high volume of GPUs in gaming would ensure its adoption by researchers.
- **12:06, 15:11** – Decided to re-engineer the entire computing stack (creating DGX) after the 2012 AlexNet breakthrough, betting that deep learning would reshape the computer industry.
- **16:49, 19:32** – Maintained commitment and invested tens of billions over 10 years based on core beliefs, even when others did not believe in it.
- **39:31** – Bet on flexible, general-purpose GPU architectures, believing that innovation (e.g., new AI models beyond Transformers) will continue.



### Risks / Open Issues



- **AI Safety (Malicious Use)**: Concerns include bias, toxicity, hallucination, generating fake information (news, images), and impersonation.
- **AI Safety (Performance Failure)**: Risk of an AI doing a task "wrongly" due to sensor failure or poor detection (e.g., a self-driving car) and causing harm.
- **AI Safety (System Failure)**: Risk of the underlying hardware (the machine) breaking down, even if the AI's logic is correct. Mitigation involves redundancy, like in autopilots.
- **Energy Limits**: The amount of computation is ultimately limited by the energy required by the laws of physics to transport and flip bits.
- **Algorithmic Scalability (Transformers)**: The "attention" mechanism in Transformers, which compares every word to every other word, becomes computationally "impossible" as context windows grow to millions of tokens.