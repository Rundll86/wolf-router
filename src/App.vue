<template>
  <div class="app-container">
    <header class="header">
      <h1>🐺 Wolf Router</h1>
      <p>智能 AI 模型路由系统</p>
    </header>
    
    <div class="chat-container">
      <div class="message-list" ref="messageList">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message-item"
          :class="{ 'user-message': msg.type === 'user', 'system-message': msg.type === 'system' }"
        >
          <div class="message-avatar">
            {{ msg.type === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div v-if="msg.type === 'user'" class="message-text">
              {{ msg.content }}
            </div>
            <div v-else>
              <div v-if="msg.route" class="route-info">
                <div class="route-label">📡 路由决策</div>
                <div class="route-model">目标模型: {{ msg.route.model }}</div>
                <div class="route-reason">路由理由: {{ msg.route.reason }}</div>
              </div>
              <div class="message-text">{{ msg.content }}</div>
            </div>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>
        
        <div v-if="isLoading" class="loading-indicator">
          <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span class="loading-text">正在分析请求并路由...</span>
        </div>
      </div>
      
      <div class="input-container">
        <input
          v-model="inputMessage"
          @keyup.enter="sendMessage"
          type="text"
          class="message-input"
          placeholder="输入你的问题..."
          :disabled="isLoading"
        />
        <button
          @click="sendMessage"
          class="send-button"
          :disabled="!inputMessage.trim() || isLoading"
        >
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">import { ref, nextTick, onMounted } from 'vue';
interface RouteInfo {
 model: string;
 reason: string;
}
interface Message {
 type: 'user' | 'system';
 content: string;
 route?: RouteInfo;
 time: string;
}
const messages = ref<Message[]>([
 {
 type: 'system',
 content: '欢迎使用 Wolf Router！请输入你的问题，我会为你选择最合适的 AI 模型来回答。',
 time: new Date().toLocaleTimeString()
 }
]);
const inputMessage = ref('');
const isLoading = ref(false);
const messageList = ref<HTMLElement | null>(null);
const API_BASE_URL = '';
function formatTime(): string {
 return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}
async function sendMessage() {
 if (!inputMessage.value.trim() || isLoading.value)
 return;
 const userMsg: Message = {
 type: 'user',
 content: inputMessage.value.trim(),
 time: formatTime()
 };
 messages.value.push(userMsg);
 inputMessage.value = '';
 isLoading.value = true;
 await scrollToBottom();
 try {
 const response = await fetch(`${API_BASE_URL}/api/chat`, {
 method: 'POST',
 headers: {
 'Content-Type': 'application/json'
 },
 body: JSON.stringify({ message: userMsg.content })
 });
 if (!response.ok) {
 throw new Error('请求失败');
 }
 const reader = response.body?.getReader();
 const decoder = new TextDecoder('utf-8');
 let systemMsg: Message | null = null;
 while (reader) {
 const { done, value } = await reader.read();
 if (done)
 break;
 const chunk = decoder.decode(value);
 const lines = chunk.split('\n').filter(line => line.trim());
 for (const line of lines) {
 try {
 const data = JSON.parse(line);
 if (data.type === 'route') {
 systemMsg = {
 type: 'system',
 content: '',
 route: {
 model: data.model,
 reason: data.reason
 },
 time: formatTime()
 };
 messages.value.push(systemMsg);
 }
 else if (data.type === 'response' && systemMsg) {
 systemMsg.content += data.content;
 }
 await scrollToBottom();
 }
 catch (e) {
 console.error('解析错误:', e);
 }
 }
 }
 }
 catch (error) {
 messages.value.push({
 type: 'system',
 content: `错误: ${error instanceof Error ? error.message : '未知错误'}`,
 time: formatTime()
 });
 }
 finally {
 isLoading.value = false;
 await scrollToBottom();
 }
}
async function scrollToBottom() {
 await nextTick();
 if (messageList.value) {
 messageList.value.scrollTop = messageList.value.scrollHeight;
 }
}
onMounted(() => {
 scrollToBottom();
});
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  text-align: center;
  padding: 20px;
  color: white;
  background: rgba(0, 0, 0, 0.2);
}

.header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
}

.header p {
  margin: 0;
  font-size: 14px;
  opacity: 0.8;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px 16px 0 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
  font-size: 32px;
  margin-right: 12px;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-text {
  background: #f1f3f4;
  padding: 12px 16px;
  border-radius: 0 16px 16px 16px;
  line-height: 1.6;
  word-break: break-word;
}

.user-message .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px 16px 0 16px;
}

.route-info {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 12px;
}

.route-label {
  font-weight: bold;
  margin-bottom: 8px;
  font-size: 14px;
}

.route-model, .route-reason {
  font-size: 13px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.route-reason {
  margin-bottom: 0;
}

.message-time {
  font-size: 12px;
  color: #9aa0a6;
  margin-top: 6px;
  text-align: right;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.6);
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-dots {
  display: flex;
  gap: 8px;
  margin-right: 12px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: loading 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
.loading-dots span:nth-child(3) { animation-delay: 0s; }

@keyframes loading {
  0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

.loading-text {
  color: #667eea;
  font-size: 14px;
}

.input-container {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.message-input {
  flex: 1;
  padding: 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 24px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.message-input:focus {
  border-color: #667eea;
}

.message-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.send-button {
  padding: 14px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .chat-container {
    padding: 10px;
  }
  
  .message-list {
    padding: 10px;
  }
  
  .input-container {
    padding: 12px;
    gap: 8px;
  }
  
  .message-input {
    padding: 12px 14px;
    font-size: 14px;
  }
  
  .send-button {
    padding: 12px 18px;
    font-size: 14px;
  }
}
</style>