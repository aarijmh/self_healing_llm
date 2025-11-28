class CallSignDemo {
    constructor() {
        this.currentStep = 0;
        this.isRunning = false;
        this.isPaused = false;
        this.stepDelay = 1500;
        
        this.steps = [
            // Phase 1: Trust Bootstrap
            {
                title: "Trust Ceremony",
                description: "OpenAI Agent establishes trust with CallSign Gateway",
                participant: "openai",
                message: "Trust ceremony: {\"ssa\": \"eyJ...\", \"attestation\": {...}, \"jwks\": {...}}",
                phase: "Trust Bootstrap"
            },
            {
                title: "Trust Handshake",
                description: "CallSign Gateway establishes trust with Bank API",
                participant: "callsign",
                message: "Trust handshake: {\"as_keys\": {...}, \"rar_schema\": {...}, \"mtls_certs\": [...]}",
                phase: "Trust Bootstrap"
            },
            {
                title: "Trust Confirmation",
                description: "Bank confirms trust establishment",
                participant: "bank",
                message: "Trust confirmation: {\"status\": \"confirmed\", \"api_contract\": {...}}",
                phase: "Trust Bootstrap"
            },
            {
                title: "Trust Bundle",
                description: "CallSign provides trust bundle to OpenAI Agent",
                participant: "callsign",
                message: "Trust bundle: {\"endpoints\": [...], \"scopes\": [...], \"policies\": [...]}",
                phase: "Trust Bootstrap"
            },
            // Phase 2: User Enrollment
            {
                title: "User Enrollment",
                description: "User enrolls with KYC and consent preferences",
                participant: "user",
                message: "Enroll: {\"kyc_data\": {...}, \"consent\": {...}, \"retention_policy\": \"30d\"}",
                phase: "User Enrollment"
            },
            {
                title: "WebAuthn Registration",
                description: "CallSign provides WebAuthn registration",
                participant: "callsign",
                message: "Registration: {\"webauthn_challenge\": \"...\", \"dashboard_url\": \"...\"}",
                phase: "User Enrollment"
            },
            {
                title: "Delegation Policy",
                description: "User creates delegation policy with limits",
                participant: "user",
                message: "Policy: {\"limits\": {\"daily\": 1000}, \"constraints\": [...], \"sca_rules\": [...]}",
                phase: "User Enrollment"
            },
            {
                title: "Policy Confirmation",
                description: "CallSign confirms policy creation",
                participant: "callsign",
                message: "Policy created: {\"policy_id\": \"pol_123\", \"revocation_handle\": \"rev_456\"}",
                phase: "User Enrollment"
            },
            // Phase 3: Payment Transaction
            {
                title: "Token Request",
                description: "OpenAI Agent requests access token",
                participant: "openai",
                message: "Token request: {\"dpop\": \"eyJ...\", \"policy_id\": \"pol_123\", \"scope\": \"payment:write\"}",
                phase: "Payment Transaction"
            },
            {
                title: "Access Token",
                description: "CallSign provides access token",
                participant: "callsign",
                message: "Access token: {\"access_token\": \"eyJ...\", \"expires_in\": 3600, \"scope\": \"payment:write\"}",
                phase: "Payment Transaction"
            },
            {
                title: "Payment Request",
                description: "OpenAI Agent makes payment request to Bank",
                participant: "openai",
                message: "Payment: {\"amount\": 100.00, \"currency\": \"USD\", \"recipient\": \"acc_789\"}",
                phase: "Payment Transaction"
            },
            {
                title: "Transaction Receipt",
                description: "Bank processes payment and returns receipt",
                participant: "bank",
                message: "Receipt: {\"txn_id\": \"tx_abc123\", \"status\": \"completed\", \"timestamp\": \"...\"}",
                phase: "Payment Transaction"
            },
            // Phase 4: Monitoring
            {
                title: "Agent Trace",
                description: "OpenAI Agent sends trace data",
                participant: "openai",
                message: "Trace: {\"request_id\": \"req_123\", \"latency_ms\": 45, \"status\": \"success\"}",
                phase: "Monitoring"
            },
            {
                title: "Auth Trace",
                description: "CallSign sends authentication trace",
                participant: "callsign",
                message: "Auth trace: {\"policy_eval_ms\": 12, \"auth_time_ms\": 8, \"decision\": \"allow\"}",
                phase: "Monitoring"
            },
            {
                title: "Transaction Trace",
                description: "Bank sends transaction trace",
                participant: "bank",
                message: "Txn trace: {\"txn_id\": \"tx_abc123\", \"amount\": 100.00, \"status\": \"completed\"}",
                phase: "Monitoring"
            },
            {
                title: "User Notification",
                description: "Monitoring system notifies user",
                participant: "monitoring",
                message: "Alert: {\"type\": \"transaction_complete\", \"txn_id\": \"tx_abc123\", \"amount\": 100.00}",
                phase: "Monitoring"
            }
        ];
        
        this.init();
    }
    
    init() {
        this.renderSteps();
        this.bindEvents();
        this.updateProgress();
    }
    
    bindEvents() {
        document.getElementById('startDemo').addEventListener('click', () => this.startDemo());
        document.getElementById('resetDemo').addEventListener('click', () => this.resetDemo());
        document.getElementById('pauseDemo').addEventListener('click', () => this.togglePause());
    }
    
    renderSteps() {
        const container = document.getElementById('step-container');
        let currentPhase = '';
        
        container.innerHTML = this.steps.map((step, index) => {
            let phaseHeader = '';
            if (step.phase && step.phase !== currentPhase) {
                currentPhase = step.phase;
                phaseHeader = `<div class="phase-header">${currentPhase}</div>`;
            }
            
            return `
                ${phaseHeader}
                <div class="step" id="step-${index}">
                    <div class="step-number">${index + 1}</div>
                    <div class="step-content">
                        <div class="step-title">${step.title}</div>
                        <div class="step-description">${step.description}</div>
                        <div class="step-payload">${step.message}</div>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    startDemo() {
        if (this.isRunning && !this.isPaused) return;
        
        if (this.isPaused) {
            this.isPaused = false;
            document.getElementById('pauseDemo').textContent = 'Pause';
            this.continueDemo();
        } else {
            this.resetDemo();
            this.isRunning = true;
            this.runStep();
        }
    }
    
    togglePause() {
        if (!this.isRunning) return;
        
        this.isPaused = !this.isPaused;
        document.getElementById('pauseDemo').textContent = this.isPaused ? 'Resume' : 'Pause';
        
        if (!this.isPaused) {
            this.continueDemo();
        }
    }
    
    continueDemo() {
        if (this.currentStep < this.steps.length && !this.isPaused) {
            setTimeout(() => this.runStep(), this.stepDelay);
        }
    }
    
    resetDemo() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentStep = 0;
        
        document.getElementById('pauseDemo').textContent = 'Pause';
        document.querySelectorAll('.participant').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.step').forEach(s => {
            s.classList.remove('active', 'completed');
        });
        
        document.getElementById('currentMessage').textContent = 'Click "Start Demo" to begin';
        this.updateProgress();
    }
    
    runStep() {
        if (this.isPaused || this.currentStep >= this.steps.length) return;
        
        const step = this.steps[this.currentStep];
        
        // Update active participant
        document.querySelectorAll('.participant').forEach(p => p.classList.remove('active'));
        document.getElementById(step.participant).classList.add('active');
        
        // Update step status
        if (this.currentStep > 0) {
            document.getElementById(`step-${this.currentStep - 1}`).classList.remove('active');
            document.getElementById(`step-${this.currentStep - 1}`).classList.add('completed');
        }
        
        document.getElementById(`step-${this.currentStep}`).classList.add('active');
        
        // Update message
        document.getElementById('currentMessage').textContent = step.message;
        
        // Update progress
        this.updateProgress();
        
        this.currentStep++;
        
        if (this.currentStep < this.steps.length) {
            setTimeout(() => this.runStep(), this.stepDelay);
        } else {
            // Demo completed
            setTimeout(() => {
                document.getElementById(`step-${this.currentStep - 1}`).classList.remove('active');
                document.getElementById(`step-${this.currentStep - 1}`).classList.add('completed');
                document.querySelectorAll('.participant').forEach(p => p.classList.remove('active'));
                document.getElementById('currentMessage').textContent = 'Demo completed! Click "Reset" to run again.';
                this.isRunning = false;
            }, this.stepDelay);
        }
    }
    
    updateProgress() {
        const progress = (this.currentStep / this.steps.length) * 100;
        document.getElementById('progressBar').style.setProperty('--progress', `${progress}%`);
        document.getElementById('progressText').textContent = `${this.currentStep} / ${this.steps.length}`;
    }
}

// Initialize demo when page loads
document.addEventListener('DOMContentLoaded', () => {
    new CallSignDemo();
});