/**
 * Discord Voice Channel 24/7 User Account Script with Web Dashboard
 * For educational and research purposes only
 * 
 * ⚠️ WARNING: Using user account tokens (selfbots) violates Discord's Terms of Service
 * This is for educational/research purposes only with dummy accounts
 * 
 * Features:
 * - Stays connected to voice channel 24/7
 * - Natural behavior patterns to minimize detection
 * - Express web dashboard for monitoring
 * - Auto-reconnection with exponential backoff
 */

import { Client } from 'discord.js-selfbot-v13';
import { 
  joinVoiceChannel, 
  VoiceConnectionStatus, 
  entersState
} from '@discordjs/voice';
import express from 'express';

// Hardcoded configuration - Replace with your actual values
// ⚠️ WARNING: Never commit real tokens to version control in production
const TOKEN = "YOUR_DISCORD_TOKEN_HERE";
const GUILD_ID = "YOUR_GUILD_ID_HERE";
const CHANNEL_ID = "YOUR_CHANNEL_ID_HERE";
const WEB_PORT = 3000;

// Configuration for natural behavior
const CONFIG = {
  // Reconnection settings with exponential backoff
  maxReconnectDelay: 300000, // 5 minutes max
  initialReconnectDelay: 5000, // 5 seconds initial
  reconnectBackoffMultiplier: 1.5,
  
  // Status update interval (appear active)
  statusUpdateInterval: 300000, // 5 minutes
  
  // Heartbeat check interval
  heartbeatInterval: 60000, // 1 minute
};

class VoiceChannelBot {
  constructor() {
    // Initialize Discord user client (selfbot)
    this.client = new Client({
      checkUpdate: false,
    });
    
    this.connection = null;
    this.reconnectAttempts = 0;
    this.isReconnecting = false;
    this.heartbeatTimer = null;
    this.statusTimer = null;
    
    // Stats for dashboard
    this.stats = {
      startTime: Date.now(),
      connectedSince: null,
      reconnections: 0,
      status: 'Starting...',
      currentChannel: null,
      uptime: 0,
    };
    
    // Initialize web dashboard
    this.initWebDashboard();
  }

  /**
   * Initialize web dashboard
   */
  initWebDashboard() {
    const app = express();
    
    // Serve static HTML dashboard
    app.get('/', (req, res) => {
      res.send(this.getDashboardHTML());
    });
    
    // API endpoint for stats
    app.get('/api/stats', (req, res) => {
      this.stats.uptime = Date.now() - this.stats.startTime;
      res.json(this.stats);
    });
    
    // API endpoint to trigger reconnect
    app.post('/api/reconnect', (req, res) => {
      console.log('🔄 Manual reconnect triggered from dashboard');
      if (this.connection) {
        this.connection.destroy();
      }
      this.handleDisconnection();
      res.json({ success: true, message: 'Reconnecting...' });
    });
    
    app.listen(WEB_PORT, () => {
      console.log(`🌐 Web dashboard running at http://localhost:${WEB_PORT}`);
    });
  }

  /**
   * Get HTML for dashboard
   */
  getDashboardHTML() {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord VC 24/7 Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        .status-connected { background: #10b981; }
        .status-connecting { background: #f59e0b; }
        .status-disconnected { background: #ef4444; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .btn:active {
            transform: translateY(0);
        }
        .warning {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #92400e;
        }
        .info-section {
            margin-top: 20px;
            padding: 20px;
            background: #f9fafb;
            border-radius: 10px;
        }
        .info-section h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e5e7eb;
        }
        .info-item:last-child {
            border-bottom: none;
        }
        .info-label {
            color: #6b7280;
        }
        .info-value {
            color: #111827;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Discord VC 24/7</h1>
        <p class="subtitle">Educational & Research Dashboard</p>
        
        <div class="status-indicator">
            <div class="status-dot" id="statusDot"></div>
            <div>
                <strong>Status:</strong> <span id="status">Loading...</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Uptime</div>
                <div class="stat-value" id="uptime">0h 0m</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Reconnections</div>
                <div class="stat-value" id="reconnections">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Connected Since</div>
                <div class="stat-value" id="connectedSince">--:--</div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Connection Info</h3>
            <div class="info-item">
                <span class="info-label">Current Channel:</span>
                <span class="info-value" id="currentChannel">Not connected</span>
            </div>
            <div class="info-item">
                <span class="info-label">User:</span>
                <span class="info-value" id="userName">Loading...</span>
            </div>
            <div class="info-item">
                <span class="info-label">Server:</span>
                <span class="info-value" id="serverName">Loading...</span>
            </div>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <button class="btn" onclick="reconnect()">🔄 Reconnect</button>
        </div>
        
        <div class="warning">
            ⚠️ <strong>Warning:</strong> This tool is for educational and research purposes only. 
            Using user account tokens (selfbots) violates Discord's Terms of Service.
        </div>
    </div>

    <script>
        function formatUptime(ms) {
            const seconds = Math.floor(ms / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);
            
            if (days > 0) return days + 'd ' + (hours % 24) + 'h';
            if (hours > 0) return hours + 'h ' + (minutes % 60) + 'm';
            return minutes + 'm ' + (seconds % 60) + 's';
        }
        
        function formatTime(timestamp) {
            if (!timestamp) return '--:--';
            const date = new Date(timestamp);
            return date.toLocaleTimeString();
        }
        
        function updateStats() {
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status').textContent = data.status;
                    document.getElementById('uptime').textContent = formatUptime(data.uptime);
                    document.getElementById('reconnections').textContent = data.reconnections;
                    document.getElementById('connectedSince').textContent = formatTime(data.connectedSince);
                    document.getElementById('currentChannel').textContent = data.currentChannel || 'Not connected';
                    
                    const dot = document.getElementById('statusDot');
                    dot.className = 'status-dot';
                    if (data.status.includes('Connected')) {
                        dot.classList.add('status-connected');
                    } else if (data.status.includes('Connecting')) {
                        dot.classList.add('status-connecting');
                    } else {
                        dot.classList.add('status-disconnected');
                    }
                })
                .catch(err => console.error('Failed to fetch stats:', err));
        }
        
        function reconnect() {
            fetch('/api/reconnect', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    alert(data.message);
                    updateStats();
                })
                .catch(err => alert('Failed to reconnect: ' + err));
        }
        
        // Update stats every 2 seconds
        updateStats();
        setInterval(updateStats, 2000);
    </script>
</body>
</html>
    `;
  }

  /**
   * Initialize the bot and connect to voice channel
   */
  async start() {
    console.log('🚀 Starting Discord VC 24/7 User Account Script...');
    console.log('⚠️  WARNING: Selfbots violate Discord ToS. For educational use only!');
    
    // Set up event handlers
    this.setupEventHandlers();
    
    // Login to Discord
    try {
      this.stats.status = 'Logging in...';
      await this.client.login(TOKEN);
    } catch (error) {
      console.error('❌ Failed to login:', error.message);
      this.stats.status = 'Login failed';
      process.exit(1);
    }
  }

  /**
   * Set up all event handlers for the bot
   */
  setupEventHandlers() {
    this.client.once('ready', () => {
      console.log(`✅ Logged in as ${this.client.user.tag}`);
      console.log(`📍 Target Guild: ${GUILD_ID}`);
      console.log(`📍 Target Channel: ${CHANNEL_ID}`);
      
      this.stats.status = 'Ready';
      
      // Connect to voice channel
      this.connectToVoiceChannel();
      
      // Start periodic tasks
      this.startHeartbeat();
    });

    // Handle disconnections
    this.client.on('disconnect', () => {
      console.log('⚠️  Client disconnected');
      this.handleDisconnection();
    });

    // Handle errors
    this.client.on('error', (error) => {
      console.error('❌ Client error:', error.message);
    });

    // Handle voice state updates
    this.client.on('voiceStateUpdate', (oldState, newState) => {
      // Check if it's our bot
      if (newState.id === this.client.user.id) {
        if (newState.channelId === null && oldState.channelId !== null) {
          console.log('⚠️  Bot was disconnected from voice channel');
          this.handleDisconnection();
        }
      }
    });

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down gracefully...');
      this.cleanup();
      process.exit(0);
    });

    process.on('SIGTERM', () => {
      console.log('\n🛑 Shutting down gracefully...');
      this.cleanup();
      process.exit(0);
    });
  }

  /**
   * Connect to the voice channel
   */
  connectToVoiceChannel() {
    try {
      this.stats.status = 'Connecting to voice...';
      
      const guild = this.client.guilds.cache.get(GUILD_ID);
      
      if (!guild) {
        console.error('❌ Guild not found. Make sure you are in the server.');
        this.stats.status = 'Guild not found';
        process.exit(1);
      }

      const channel = guild.channels.cache.get(CHANNEL_ID);
      
      if (!channel) {
        console.error('❌ Voice channel not found. Check your CHANNEL_ID.');
        this.stats.status = 'Channel not found';
        process.exit(1);
      }

      if (channel.type !== 2 && channel.type !== 13) { // 2 = GUILD_VOICE, 13 = GUILD_STAGE_VOICE
        console.error('❌ Channel is not a voice or stage voice channel.');
        this.stats.status = 'Invalid channel type';
        process.exit(1);
      }

      console.log(`🔊 Connecting to voice channel: ${channel.name}`);
      
      // Update stats
      this.stats.currentChannel = channel.name;

      this.connection = joinVoiceChannel({
        channelId: CHANNEL_ID,
        guildId: GUILD_ID,
        adapterCreator: guild.voiceAdapterCreator,
        selfDeaf: false, // Not deafened to appear more natural
        selfMute: true,  // Muted to not transmit audio
      });

      this.setupVoiceConnectionHandlers();
      
      // Reset reconnect attempts on successful connection
      this.reconnectAttempts = 0;
      this.isReconnecting = false;
      this.stats.connectedSince = Date.now();
      this.stats.status = 'Connected to voice';

    } catch (error) {
      console.error('❌ Failed to connect to voice channel:', error.message);
      this.stats.status = 'Connection failed';
      this.scheduleReconnect();
    }
  }

  /**
   * Set up handlers for voice connection events
   */
  setupVoiceConnectionHandlers() {
    if (!this.connection) return;

    this.connection.on(VoiceConnectionStatus.Ready, () => {
      console.log('✅ Voice connection is ready');
    });

    this.connection.on(VoiceConnectionStatus.Disconnected, async () => {
      console.log('⚠️  Voice connection disconnected');
      
      try {
        // Try to reconnect within 5 seconds
        await Promise.race([
          entersState(this.connection, VoiceConnectionStatus.Signalling, 5000),
          entersState(this.connection, VoiceConnectionStatus.Connecting, 5000),
        ]);
        // If we reach here, connection is recovering
        console.log('🔄 Voice connection is recovering...');
      } catch (error) {
        // Connection didn't recover, reconnect
        console.log('⚠️  Voice connection did not recover, reconnecting...');
        this.connection.destroy();
        this.handleDisconnection();
      }
    });

    this.connection.on(VoiceConnectionStatus.Destroyed, () => {
      console.log('⚠️  Voice connection destroyed');
      this.handleDisconnection();
    });

    this.connection.on('error', (error) => {
      console.error('❌ Voice connection error:', error.message);
      this.handleDisconnection();
    });
  }

  /**
   * Handle disconnection and schedule reconnection
   */
  handleDisconnection() {
    if (this.isReconnecting) return;
    
    this.isReconnecting = true;
    this.stats.status = 'Disconnected, reconnecting...';
    this.stats.reconnections++;
    this.scheduleReconnect();
  }

  /**
   * Schedule a reconnection with exponential backoff
   */
  scheduleReconnect() {
    const delay = Math.min(
      CONFIG.initialReconnectDelay * Math.pow(CONFIG.reconnectBackoffMultiplier, this.reconnectAttempts),
      CONFIG.maxReconnectDelay
    );

    this.reconnectAttempts++;
    this.stats.status = `Reconnecting in ${Math.round(delay / 1000)}s (Attempt ${this.reconnectAttempts})`;
    
    console.log(`🔄 Reconnecting in ${Math.round(delay / 1000)} seconds... (Attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      if (this.client.isReady()) {
        this.connectToVoiceChannel();
      } else {
        console.log('⚠️  Client not ready, waiting...');
        this.stats.status = 'Client not ready';
        this.scheduleReconnect();
      }
    }, delay);
  }

  /**
   * Start heartbeat to check connection status
   */
  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      if (!this.connection || this.connection.state.status === VoiceConnectionStatus.Destroyed) {
        console.log('💓 Heartbeat: Connection lost, attempting to reconnect...');
        this.handleDisconnection();
      } else {
        console.log(`💓 Heartbeat: Connection alive (${this.connection.state.status})`);
      }
    }, CONFIG.heartbeatInterval);
  }

  /**
   * Clean up resources
   */
  cleanup() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    
    if (this.connection) {
      this.connection.destroy();
    }
    
    this.stats.status = 'Shutting down';
    this.client.destroy();
  }
}

// Start the bot
const bot = new VoiceChannelBot();
bot.start().catch((error) => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
