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
        const streamsList = document.getElementById('streams-list');
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

        // Render stream links
        streamsList.innerHTML = '';

        this.streamsData.sources.forEach(stream => {
            const streamLink = this.createStreamLink(stream);
            streamsList.appendChild(streamLink);
        });

        streamsList.classList.remove('hidden');
    }

    createStreamLink(stream) {
        const platformClass = `platform-${stream.platform.toLowerCase().replace('.', '')}`;
        
        // For Twitch, use direct channel URL
        let watchUrl = stream.url;
        if (stream.platform === 'Twitch' && stream.channel) {
            watchUrl = `https://www.twitch.tv/${stream.channel}`;
        }

        const link = document.createElement('a');
        link.href = watchUrl;
        link.target = '_blank'; // Opens in new tab
        link.className = 'stream-link-item';
        
        link.innerHTML = `
            <div class="stream-link-header">
                <div class="stream-name">${stream.name}</div>
                <div class="platform-badge ${platformClass}">${stream.platform}</div>
            </div>
            ${stream.channel ? `<div class="stream-channel">${stream.channel}</div>` : ''}
            <div class="stream-info">Click to open stream in new tab</div>
        `;

        return link;
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
