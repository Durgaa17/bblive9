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
        const embedsContainer = document.getElementById('embeds-container');
        const linksContainer = document.getElementById('links-container');
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

        // Clear containers
        embedsContainer.innerHTML = '';
        linksContainer.innerHTML = '';

        // Separate streams into embeds and links
        const embedStreams = [];
        const linkStreams = [];

        this.streamsData.sources.forEach(stream => {
            if (stream.platform === 'Twitch') {
                linkStreams.push(stream);
            } else {
                embedStreams.push(stream);
            }
        });

        // Render embedded players at top
        if (embedStreams.length > 0) {
            embedStreams.forEach(stream => {
                const streamEmbed = this.createStreamEmbed(stream);
                embedsContainer.appendChild(streamEmbed);
            });
            document.getElementById('embeds-section').classList.remove('hidden');
        }

        // Render Twitch links at bottom
        if (linkStreams.length > 0) {
            linkStreams.forEach(stream => {
                const streamLink = this.createTwitchLink(stream);
                linksContainer.appendChild(streamLink);
            });
            document.getElementById('links-section').classList.remove('hidden');
        }

        // Show main container
        document.getElementById('streams-container').classList.remove('hidden');
    }

    createTwitchLink(stream) {
        const platformClass = `platform-${stream.platform.toLowerCase()}`;
        const watchUrl = `https://www.twitch.tv/${stream.channel}`;

        const link = document.createElement('a');
        link.href = watchUrl;
        link.target = '_blank';
        link.className = 'stream-link-item';
        
        link.innerHTML = `
            <div class="stream-link-header">
                <div class="stream-name">${stream.name}</div>
                <div class="platform-badge ${platformClass}">${stream.platform}</div>
            </div>
            <div class="stream-channel">${stream.channel}</div>
            <div class="stream-info">Click to open Twitch stream in new tab</div>
        `;

        return link;
    }

    createStreamEmbed(stream) {
        const platformClass = `platform-${stream.platform.toLowerCase().replace('.', '')}`;

        const embedCard = document.createElement('div');
        embedCard.className = 'stream-embed-card';
        
        embedCard.innerHTML = `
            <div class="stream-header">
                <div class="stream-name">${stream.name}</div>
                <div class="platform-badge ${platformClass}">${stream.platform}</div>
            </div>
            
            ${stream.channel ? `<div class="stream-channel">${stream.channel}</div>` : ''}
            
            <div class="iframe-container">
                <iframe 
                    src="${stream.embed_url}" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen
                    loading="lazy">
                </iframe>
            </div>
            
            <a href="${stream.url}" target="_blank" class="stream-link">
                🔗 Open ${stream.platform} in new tab
            </a>
        `;

        return embedCard;
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
