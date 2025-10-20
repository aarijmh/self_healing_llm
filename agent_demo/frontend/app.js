// Banking Agent Demo - Frontend Application
const API_URL = 'http://localhost:5000';
let socket;
let currentSteps = [];

// Initialize Socket.IO connection
function initializeSocket() {
	socket = io(API_URL);
	
	socket.on('connect', () => {
		console.log('Connected to backend');
		addLog('System', 'Connected to Banking Agent Demo Server', 'success');
	});
	
	socket.on('step_update', (data) => {
		handleStepUpdate(data);
	});
	
	socket.on('disconnect', () => {
		console.log('Disconnected from backend');
		addLog('System', 'Disconnected from server', 'error');
	});
}

// Handle step updates from backend
function handleStepUpdate(data) {
	const { step, status, data: stepData } = data;
	
	// Highlight active entity
	highlightEntity(step);
	
	// Add step to process flow
	addProcessStep(step, status, stepData);
	
	// Update results panel
	updateResults(step, status, stepData);
	
	// Handle specific steps
	if (step === 'search_amazon' || step === 'search_bestbuy' || step === 'search_target') {
		displayProducts(stepData.products, step.replace('search_', ''));
	}
	
	if (step === 'purchase_complete' && status === 'completed') {
		showTransactionSummary(stepData);
	}
	
	// Update account balance
	if (stepData.new_balance !== undefined) {
		updateBalance(stepData.new_balance);
	}
}

// Add process step to UI
function addProcessStep(step, status, data) {
	const stepsContainer = document.getElementById('process-steps');
	
	// Check if step already exists
	let stepElement = document.getElementById(`step-${step}`);
	
	if (!stepElement) {
		stepElement = document.createElement('div');
		stepElement.id = `step-${step}`;
		stepElement.className = 'step-card p-4 rounded-lg slide-in';
		stepsContainer.appendChild(stepElement);
	}
	
	// Update step status
	stepElement.className = 'step-card p-4 rounded-lg slide-in';
	
	let icon, iconColor, statusText;
	
	if (status === 'started') {
		stepElement.classList.add('active');
		icon = 'fa-spinner fa-spin';
		iconColor = 'text-blue-600';
		statusText = 'In Progress';
	} else if (status === 'completed') {
		stepElement.classList.add('completed');
		icon = 'fa-check-circle';
		iconColor = 'text-green-600';
		statusText = 'Completed';
	} else if (status === 'failed') {
		stepElement.classList.add('failed');
		icon = 'fa-times-circle';
		iconColor = 'text-red-600';
		statusText = 'Failed';
	}
	
	const stepTitle = formatStepName(step);
	
	stepElement.innerHTML = `
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-3">
				<i class="fas ${icon} ${iconColor} text-xl"></i>
				<div>
					<div class="font-semibold text-gray-800">${stepTitle}</div>
					<div class="text-xs text-gray-500">${statusText}</div>
				</div>
			</div>
			<div class="text-xs text-gray-400">${new Date().toLocaleTimeString()}</div>
		</div>
		${data && Object.keys(data).length > 0 ? `
			<div class="mt-2 text-xs text-gray-600 bg-gray-50 p-2 rounded">
				${formatStepData(data)}
			</div>
		` : ''}
	`;
	
	// Scroll to bottom
	stepsContainer.scrollTop = stepsContainer.scrollHeight;
}

// Format step name for display
function formatStepName(step) {
	const names = {
		'app_download': 'App Download & Installation',
		'identity_verification': 'Identity Verification',
		'device_registration': 'Device Registration',
		'biometric_enrollment': 'Biometric Enrollment',
		'agent_registration': 'Agent Registration',
		'delegation_auth': 'Delegation Authentication',
		'delegation_registration': 'Delegation Registration',
		'authentication': 'User Authentication',
		'product_search': 'Product Search',
		'search_amazon': 'Search Amazon',
		'search_bestbuy': 'Search BestBuy',
		'search_target': 'Search Target',
		'transaction_auth': 'Transaction Authorization',
		'payment_auth': 'Payment Authentication',
		'payment_token': 'Payment Token Generation',
		'payment_processing': 'Payment Processing',
		'bank_transaction': 'Bank Transaction',
		'order_creation': 'Order Creation',
		'purchase_complete': 'Purchase Complete'
	};
	
	return names[step] || step.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Format step data for display
function formatStepData(data) {
	const important = {};
	
	// Extract important fields
	if (data.token) important['Token'] = data.token.substring(0, 20) + '...';
	if (data.agent_id) important['Agent ID'] = data.agent_id;
	if (data.delegation_id) important['Delegation ID'] = data.delegation_id;
	if (data.spending_limit) important['Spending Limit'] = `$${data.spending_limit}`;
	if (data.amount) important['Amount'] = `$${data.amount}`;
	if (data.merchant) important['Merchant'] = data.merchant;
	if (data.order_id) important['Order ID'] = data.order_id;
	if (data.transaction_id) important['Transaction ID'] = data.transaction_id;
	if (data.total_found) important['Products Found'] = data.total_found;
	if (data.authorized !== undefined) important['Authorized'] = data.authorized ? 'Yes' : 'No';
	
	return Object.entries(important)
		.map(([key, value]) => `<strong>${key}:</strong> ${value}`)
		.join(' • ');
}

// Update results panel
function updateResults(step, status, data) {
	const resultsPanel = document.getElementById('results-panel');
	
	if (status === 'completed' && data && Object.keys(data).length > 0) {
		const resultCard = document.createElement('div');
		resultCard.className = 'bg-gray-50 p-4 rounded-lg border-l-4 border-green-500 slide-in';
		
		resultCard.innerHTML = `
			<div class="font-semibold text-gray-800 mb-2">
				<i class="fas fa-check-circle text-green-600 mr-2"></i>
				${formatStepName(step)}
			</div>
			<pre class="text-xs text-gray-600 overflow-x-auto">${JSON.stringify(data, null, 2)}</pre>
		`;
		
		// Remove placeholder if exists
		if (resultsPanel.querySelector('.text-gray-400')) {
			resultsPanel.innerHTML = '';
		}
		
		resultsPanel.appendChild(resultCard);
		resultsPanel.scrollTop = resultsPanel.scrollHeight;
	}
}

// Highlight active entity
function highlightEntity(step) {
	// Remove all active states
	document.querySelectorAll('.entity-box').forEach(box => {
		box.classList.remove('active');
	});
	
	// Map steps to entities
	const entityMap = {
		'biometric_enrollment': 'callsign',
		'delegation_auth': 'callsign',
		'authentication': 'callsign',
		'payment_auth': 'callsign',
		'agent_registration': 'bankmcp',
		'delegation_registration': 'bankmcp',
		'transaction_auth': 'bankmcp',
		'payment_token': 'hsm',
		'identity_verification': 'bank',
		'bank_transaction': 'bank',
		'search_amazon': 'amazon',
		'payment_processing': 'payment',
		'order_creation': 'amazon'
	};
	
	const entityId = entityMap[step];
	if (entityId) {
		const entityBox = document.getElementById(`entity-${entityId}`);
		if (entityBox) {
			entityBox.classList.add('active');
		}
	}
}

// Display products
function displayProducts(products, merchant) {
	const productsSection = document.getElementById('products-section');
	const productsGrid = document.getElementById('products-grid');
	
	if (!products || products.length === 0) return;
	
	productsSection.classList.remove('hidden');
	
	products.forEach(product => {
		const productCard = document.createElement('div');
		productCard.className = 'product-card bg-white border-2 border-gray-200 rounded-lg p-4';
		
		const merchantColors = {
			'amazon': 'orange',
			'bestbuy': 'blue',
			'target': 'red'
		};
		
		const color = merchantColors[merchant] || 'gray';
		
		productCard.innerHTML = `
			<div class="bg-${color}-50 rounded-lg p-4 mb-3 text-center">
				<i class="fas fa-laptop text-4xl text-${color}-600"></i>
			</div>
			<h3 class="font-bold text-lg mb-2">${product.name}</h3>
			<div class="flex items-center justify-between mb-2">
				<span class="text-2xl font-bold text-${color}-600">$${product.price}</span>
				<span class="text-yellow-500">
					${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}
				</span>
			</div>
			<div class="text-sm text-gray-600 mb-3">
				<i class="fas fa-store mr-1"></i> ${merchant.toUpperCase()}
			</div>
			<div class="text-xs text-gray-500">
				Category: ${product.category}
			</div>
		`;
		
		productsGrid.appendChild(productCard);
	});
}

// Show transaction summary
function showTransactionSummary(data) {
	const summarySection = document.getElementById('transaction-summary');
	const summaryDetails = document.getElementById('summary-details');
	
	summarySection.classList.remove('hidden');
	
	summaryDetails.innerHTML = `
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
			<div class="bg-white bg-opacity-20 rounded-lg p-4">
				<div class="text-sm opacity-80">Product</div>
				<div class="text-xl font-bold">${data.product.name}</div>
			</div>
			<div class="bg-white bg-opacity-20 rounded-lg p-4">
				<div class="text-sm opacity-80">Amount</div>
				<div class="text-xl font-bold">$${data.product.price}</div>
			</div>
			<div class="bg-white bg-opacity-20 rounded-lg p-4">
				<div class="text-sm opacity-80">Order ID</div>
				<div class="text-xl font-bold">${data.order.order_id}</div>
			</div>
			<div class="bg-white bg-opacity-20 rounded-lg p-4">
				<div class="text-sm opacity-80">Delivery</div>
				<div class="text-xl font-bold">${data.order.estimated_delivery}</div>
			</div>
		</div>
		<div class="mt-6 bg-white bg-opacity-20 rounded-lg p-4">
			<div class="text-sm opacity-80">New Account Balance</div>
			<div class="text-3xl font-bold">$${data.new_balance.toFixed(2)}</div>
		</div>
	`;
}

// Update balance display
function updateBalance(balance) {
	const balanceElement = document.getElementById('balance');
	balanceElement.textContent = `$${balance.toFixed(2)}`;
}

// Add log message
function addLog(source, message, type = 'info') {
	console.log(`[${source}] ${message}`);
}

// API Calls
async function runSetup() {
	resetDemo();
	try {
		const response = await fetch(`${API_URL}/api/demo/setup`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});
		const result = await response.json();
		console.log('Setup completed:', result);
	} catch (error) {
		console.error('Setup failed:', error);
		alert('Setup failed. Make sure the backend server is running.');
	}
}

async function runDelegation() {
	try {
		const response = await fetch(`${API_URL}/api/demo/delegate`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				spending_limit: 5000,
				categories: ['electronics', 'home']
			})
		});
		const result = await response.json();
		console.log('Delegation completed:', result);
	} catch (error) {
		console.error('Delegation failed:', error);
		alert('Delegation failed. Make sure the backend server is running.');
	}
}

async function runPurchase() {
	try {
		const response = await fetch(`${API_URL}/api/demo/purchase`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				query: 'laptop',
				max_price: 2000
			})
		});
		const result = await response.json();
		console.log('Purchase completed:', result);
	} catch (error) {
		console.error('Purchase failed:', error);
		alert('Purchase failed. Make sure the backend server is running.');
	}
}

async function runCompleteDemo() {
	resetDemo();
	
	// Run setup
	await runSetup();
	await sleep(2000);
	
	// Run delegation
	await runDelegation();
	await sleep(2000);
	
	// Run purchase
	await runPurchase();
}

function resetDemo() {
	// Clear process steps
	document.getElementById('process-steps').innerHTML = '';
	
	// Clear results
	document.getElementById('results-panel').innerHTML = `
		<div class="text-center text-gray-400 py-12">
			<i class="fas fa-info-circle text-5xl mb-4"></i>
			<p>Start a demo to see live results</p>
		</div>
	`;
	
	// Hide products section
	document.getElementById('products-section').classList.add('hidden');
	document.getElementById('products-grid').innerHTML = '';
	
	// Hide transaction summary
	document.getElementById('transaction-summary').classList.add('hidden');
	
	// Remove entity highlights
	document.querySelectorAll('.entity-box').forEach(box => {
		box.classList.remove('active');
	});
	
	// Reset balance
	updateBalance(15000);
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
	initializeSocket();
	console.log('Banking Agent Demo initialized');
});
