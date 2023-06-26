var app = new Vue({
	el:"#app",
	data(){
		return {
			deck:{
				id:"",
				name:"",
				user_id:"",
				last_reviewed:"",
				total_score:"",
			},
			decks:[],
		}
	},
	async created(){
		await this.getDecks()
	},
	methods:{
		async getDecks(){
			const response = await fetch(window.location, {
				method:"get",
				headers:{
					"X-Requested-With":"XMLHttpRequest"
				}
			})
			this.decks = await response.json()
			console.log(this.decks)
		},
		async createDeck(){
			await this.getDecks()
			console.log(window.location)
			const response = await fetch(window.location.origin + "/deck/create",{
				method:"post",
				headers:{
					"Content-Type":"application/json",
					"X-Requested-With":"XMLHttpRequest"
				},
				body: JSON.stringify(this.deck)
			})

			await this.getDecks()
			this.deck.name=""
		},
		async deleteDeck(deck){
			console.log(window.location)
			const response = await fetch(window.location.origin + "/deck/delete",{
				method:"post",
				headers:{
					"Content-Type":"application/json",
					"X-Requested-With":"XMLHttpRequest"
				},
				body: JSON.stringify(deck)
			})

			await this.getDecks()
		},
		async exportCSV(){
			const response = await fetch(window.location,{
				method:"get",
				headers:{
					"ExportCSV":"True",
					"X-Requested-With":"XMLHttpRequest"
				},
			})
		},
	},
	delimiters:['{','}']
})