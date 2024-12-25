const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            categories: [],
            dataSources: {},
            activeTab: 'category',
            config: {
                environment: 'sandbox',
                category: '',
                sources: {},
                customCriteria: '',
                agentUrl: '',
                mode: 'standard'
            },
            defaultCriteria: '',
            parsedCriteria: null,
            results: null,
            loading: false
        }
    },
    computed: {
        isConfigValid() {
            return this.config.category && 
                   this.config.agentUrl &&
                   Object.keys(this.config.sources).length > 0
        }
    },
    methods: {
        async selectCategory(categoryId) {
            this.config.category = categoryId
            const response = await axios.get(`/api/criteria/${categoryId}`)
            this.defaultCriteria = response.data.default_criteria
        },
        
        async previewCriteria() {
            if (!this.config.customCriteria) {
                this.parsedCriteria = null
                return
            }
            
            try {
                const response = await axios.post('/api/parse_criteria', {
                    criteria: this.config.customCriteria
                })
                this.parsedCriteria = JSON.stringify(response.data, null, 2)
            } catch (error) {
                console.error('Error parsing criteria:', error)
            }
        },
        
        async runBenchmark() {
            this.loading = true
            try {
                const response = await axios.post('/api/run_benchmark', this.config)
                this.results = JSON.stringify(response.data, null, 2)
            } catch (error) {
                console.error('Error running benchmark:', error)
            } finally {
                this.loading = false
            }
        }
    },
    async mounted() {
        // Load initial data
        const response = await fetch('/')
        const data = await response.json()
        this.categories = data.categories
        this.dataSources = data.data_sources
        
        // Initialize source configs
        for (const source in this.dataSources) {
            this.config.sources[source] = {}
        }
    }
})

app.mount('#app') 