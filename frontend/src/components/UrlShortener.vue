<template>
        <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <h1 class="text-2xl font-bold mb-4 text-center text-gray-800">URL Shortener</h1>
            <form @submit.prevent="shortenUrl" class="flex flex-col space-y-4">
                <input v-model="originalUrl" type="text" placeholder="Enter URL" required
                    class="border border-gray-300 rounded p-2" />
                <button type="submit" class="bg-blue-500 text-white rounded p-2 hover:bg-blue-600">Shorten</button>
            </form>
            <div v-if="shortenedUrl" class="mt-4">
                <p class="text-gray-700 mb-2">Shortened URL:</p>
                <div class="flex items-center space-x-2">
                    <input v-model="shortenedUrl" readonly class="border border-gray-300 rounded p-2 flex-grow" />
                    <button @click="copyToClipboard"
                        class="bg-green-500 text-white rounded p-2 hover:bg-green-600">Copy</button>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            originalUrl: '',
            shortenedUrl: ''
        };
    },
    methods: {
        async shortenUrl() {
            try {
                const response = await axios.post('/api/shorten', {
                    url: this.originalUrl
                });
                this.shortenedUrl = response.data.shortened_url;
            } catch (error) {
                console.error("There was an error shortening the URL:", error);
            }
        },
        copyToClipboard() {
            navigator.clipboard.writeText(this.shortenedUrl).then(() => {
                alert('Copied to clipboard');
            });
        }
    }
};
</script>

<style scoped>
/* Additional styles if needed */
</style>
