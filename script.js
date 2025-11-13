class StreamManager {
    constructor() {
        this.streamsData = null;
        this.init();
    }

    async init() {
        await this.loadStreams();
        this.setupAutoRefresh();
    }

    async loadStreams() {
        try {
            // Add cache busting parameter
            const response = await fetch('./streams.json?' + new Date().getTime());
            
            if (!response.ok) {
                throw new Error('Failed to fetch stream data');
            }
            
            this.streamsData = await response.json();
            this.renderStreams();
            
        } catch (error) {
            console.error('Error loading streams:', error);
            this.showError();
        }
    }

    renderStreams() {
        const loadingEl = document.getElementById('loading');
        const errorEl = document.getElementById('error');
        const streamsContainer = document.getElementById('streams-container');
        const noStreamsEl = document.getElementById('no-streams');
        const lastUpdatedEl = document.getElementById('lastUpdated');

        loadingEl.classList.add('hidden');
        errorEl.classList.add('hidden');

        // Update last updated time
        if (this.streamsData.last_updated) {
            const date = new Date(this.streamsData.last_updated);
            lastUpdatedEl.textContent = date.toLocaleString();
        }

        // Check if we have streams
        if (!this.streamsData.sources || this.streamsData.sources.length === 0) {
            noStreamsEl.classList.remove('hidden');
            return;
        }

        // Render streams
        const streamsGrid = document.getElementById('streamsGrid');
        streamsGrid.innerHTML = '';

        this.streamsData.sources.forEach(stream => {
            const streamCard = this.createStreamCard(stream);
            streamsGrid.appendChild(streamCard);
        });

        streamsContainer.classList.remove('hidden');
    }

    createStreamCard(stream) {
        const card = document.createElement('div');
        card.className = 'stream-card';

        const platformClass = `platform-${stream.platform.toLowerCase().replace('.', '')}`;

        card.innerHTML = `
            <div class="stream-header">
                <div class="stream-name">${stream.name}</div>
                <div class="platform-badge ${platformClass}">${stream.platform}</div>
            </div>
            
            ${stream.channel ? `<div class="stream-channel">Channel: ${stream.channel}</div>` : ''}
            
            <div class="iframe-container">
                <iframe 
                    src="${stream.embed_url}" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen
                    loading="lazy">
                </iframe>
            </div>
            
            <a href="${stream.url}" target="_blank" class="stream-link">
                🔗 Open ${stream.platform} Stream
            </a>
        `;

        return card;
    }

    showError() {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('error').classList.remove('hidden');
    }

    setupAutoRefresh() {
        // Refresh every 30 minutes
        setInterval(() => {
            this.loadStreams();
        }, 30 * 60 * 1000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new StreamManager();
});
