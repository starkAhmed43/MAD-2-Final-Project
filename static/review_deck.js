var app = new Vue({
	el:"#app",
	data(){
		return{
			deck:"",
			cards:[],
		}
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
			console.log(this.cards)
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
		setDifficulty(card, value){
			console.log(card.id,"before",card.difficulty)
			card.difficulty = value
			console.log(card.id,"after",card.difficulty)
		},
		async submitReview(){
			const response = await fetch(window.location,{
				method:"post",
				headers:{
					"Content-Type":"application/json",
					"X-Requested-With":"XMLHttpRequest"
				},
				body: JSON.stringify(this.cards)
			})
			url = await response.json()
			console.log(url)
			window.location.href=url
		}
	},
	delimiters:['{','}']
})