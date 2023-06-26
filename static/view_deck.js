var app = new Vue({
	el:"#app",
	data(){
		return{
			card:{
				id:"",
				deck_id : "",
				question : "",
				answer : "",
				difficulty : "",
				last_reviewed : "",
				last_score : "",
			},
			deck:{
				id:"",
				name:"",
				user_id:"",
				last_reviewed:"",
				total_score:"",
			},
			cards:[],
		}
	},
	async serverPrefetch(){
		await this.getCards()
		await this.getDeck()
	},
	async created(){
		await this.getCards()
		await this.getDeck()
	},
	methods:{
		async getCards(){
			const response = await fetch(window.location, {
				method:"get",
				headers:{
					"X-Requested-With":"XMLHttpRequest",
					"TYPE":"Card"
				}
			})
			this.cards = await response.json()
		},
		async getDeck(){
			const response = await fetch(window.location, {
				method:"get",
				headers:{
					"X-Requested-With":"XMLHttpRequest",
					"TYPE":"Deck"
				}
			})
			this.deck = await response.json()
		},
		async createCard(){
			await this.getCards()
			await this.getDeck()
			const response = await fetch(window.location.origin + "/deck/"+(this.deck.id)+"/create",{
				method:"post",
				headers:{
					"Content-Type":"application/json",
					"X-Requested-With":"XMLHttpRequest"
				},
				body: JSON.stringify(this.card)
			})

			await this.getCards()
			this.card.question=""
			this.card.answer=""
		},
		async deleteCard(card){
			const response = await fetch(window.location.origin + "/deck/"+(this.deck.id)+"/delete",{
				method:"post",
				headers:{
					"Content-Type":"application/json",
					"X-Requested-With":"XMLHttpRequest"
				},
				body: JSON.stringify(card)
			})

			await this.getCards()
		},
	},
	delimiters:['{','}']
})