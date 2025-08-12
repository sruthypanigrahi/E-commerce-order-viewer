let currentCustomerId = null;

// Milestone 3: Basic User Interface
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    // Search functionality
    searchInput.addEventListener('input', async function() {
        const query = this.value.trim();
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        try {
            const customers = await fetch(`/search?q=${encodeURIComponent(query)}`).then(r => r.json());
            displaySearchResults(customers);
        } catch (error) {
            console.error('Search failed:', error);
        }
    });
    
    // Status filter
    document.getElementById('statusFilter').addEventListener('change', () => {
        if (currentCustomerId) loadOrders(currentCustomerId);
    });
    
    // Modal close
    document.querySelector('.close').onclick = () => {
        document.getElementById('orderModal').style.display = 'none';
    };
    
    window.onclick = (e) => {
        const modal = document.getElementById('orderModal');
        if (e.target === modal) modal.style.display = 'none';
    };
});

function displaySearchResults(customers) {
    const searchResults = document.getElementById('searchResults');
    
    if (customers.length === 0) {
        searchResults.style.display = 'none';
        return;
    }
    
    searchResults.innerHTML = customers.map(customer => 
        `<div class="search-result-item" onclick="selectCustomer(${customer._id}, '${customer.name}')">
            ${customer.name} (${customer.email})
        </div>`
    ).join('');
    
    searchResults.style.display = 'block';
}

// Milestone 4: End-to-End Flow
async function selectCustomer(customerId, customerName) {
    currentCustomerId = customerId;
    document.getElementById('searchResults').style.display = 'none';
    document.getElementById('searchInput').value = customerName;
    
    // Show customer info
    document.getElementById('customerName').textContent = customerName;
    document.getElementById('customerInfo').style.display = 'block';
    
    // Load insights and orders
    await loadCustomerData(customerId);
}

async function loadCustomerData(customerId) {
    try {
        // Load insights
        const insights = await fetch(`/users/${customerId}/insights`).then(r => r.json());
        displayInsights(insights);
        
        // Load orders
        await loadOrders(customerId);
        
        // Show panels
        document.getElementById('insightsPanel').style.display = 'block';
        document.getElementById('filtersSection').style.display = 'block';
        document.getElementById('ordersList').style.display = 'block';
        
    } catch (error) {
        console.error('Failed to load customer data:', error);
    }
}

function displayInsights(insights) {
    document.getElementById('totalSpent').textContent = `$${insights.total_spent}`;
    document.getElementById('topCategory').textContent = insights.most_bought_category || '-';
    document.getElementById('avgGap').textContent = `${insights.average_gap} days`;
    
    // Super Coins and Loyalty Tier
    document.getElementById('superCoins').textContent = `🪙 ${insights.super_coins} Super Coins`;
    
    const tierElement = document.getElementById('loyaltyTier');
    tierElement.textContent = insights.loyalty_tier;
    tierElement.className = `tier-badge tier-${insights.loyalty_tier.toLowerCase()}`;
}

async function loadOrders(customerId) {
    try {
        const status = document.getElementById('statusFilter').value;
        const params = status ? `?status=${status}` : '';
        
        const orders = await fetch(`/users/${customerId}/orders${params}`).then(r => r.json());
        displayOrders(orders);
    } catch (error) {
        console.error('Failed to load orders:', error);
    }
}

function displayOrders(orders) {
    const container = document.getElementById('ordersContainer');
    
    if (orders.length === 0) {
        container.innerHTML = '<p>No orders found.</p>';
        return;
    }
    
    container.innerHTML = orders.map(order => `
        <div class="order-item" onclick="showOrderDetails('${order.id}')">
            <div class="order-info">
                <div class="order-id">${order.id}</div>
                <div class="order-date">${new Date(order.date).toLocaleDateString()}</div>
            </div>
            <div>
                <span class="order-amount">$${order.amount}</span>
                <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
            </div>
        </div>
    `).join('');
}

// Show order items in modal
async function showOrderDetails(orderId) {
    try {
        const items = await fetch(`/orders/${orderId}/items`).then(r => r.json());
        
        document.getElementById('modalOrderId').textContent = `Order ${orderId}`;
        
        const container = document.getElementById('orderItemsContainer');
        container.innerHTML = items.map(item => `
            <div class="item-row">
                <div class="item-info">
                    <div style="font-weight: bold;">${item.product}</div>
                    <div style="color: #666; font-size: 14px;">${item.category} • Qty: ${item.quantity}</div>
                </div>
                <div class="item-price">$${item.price}</div>
            </div>
        `).join('');
        
        document.getElementById('orderModal').style.display = 'block';
    } catch (error) {
        console.error('Failed to load order details:', error);
    }
}

// Hide search results when clicking outside
document.addEventListener('click', function(e) {
    const searchResults = document.getElementById('searchResults');
    if (searchResults && !e.target.closest('.search-section')) {
        searchResults.style.display = 'none';
    }
});