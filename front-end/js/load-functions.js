var data = {'total_tweets': {'N': '1135'}, 'hashtag_5_percentage': {'S': '90%'}, 'followers': {'N': '32902'}, 'random_tweet_id': {'N': '1354383251146592259'}, 'hashtag_1_count': {'N': '21'}, 'hashtag_1_percentage': {'S': '100%'}, 'lang_labels': {'L': [{'S': 'ja'}, {'S': 'en'}, {'S': 'in'}, {'S': 'nl'}, {'S': 'Other'}]}, 'hashtag_3_hashtag': {'S': '東京'}, 'date': {'S': '02/02/2021'}, 
'hashtag_4_percentage': {'S': '90%'}, 'hashtag_2_hashtag': {'S': 'バランスス タイル'}, 'retweets': {'L': [{'N': '30'}, {'N': '17'}, {'N': '40'}, {'N': '28'}, {'N': '27'}, {'N': '23'}, {'N': '29'}, {'N': '24'}, {'N': '27'}, {'N': '35'}, {'N': '51'}, {'N': '43'}]}, 'hashtag_1_hashtag': {'S': 'balancestyle'}, 
'random_user_name': {'S': '____47mon'}, 'random_tweet_followers': {'N': '1524'}, 'hashtag_3_count': {'N': '19'}, 'hashtag_2_count': {'N': '20'}, 'hashtag_3_percentage': {'S': '90%'}, 'most_retweeted_id': {'S': '1338802517665345537'}, 'most_favourited_id': {'S': '1270360968065953792'}, 'hashtag_4_count': {'N': '19'}, 'hashtag_5_hashtag': {'S': '名古屋'}, 'hashtag_4_hashtag': {'S': '大阪'}, 'lang_data': {'L': [{'N': '905'}, {'N': '135'}, {'N': '20'}, {'N': '16'}, {'N': '59'}]}, 'hashtag_5_count': {'N': '19'}, 'retweet_count': {'N': '388'}, 'labels': {'L': [{'S': '02-03-2020'}, {'S': '02-04-2020'}, {'S': '02-05-2020'}, {'S': '02-06-2020'}, {'S': '02-07-2020'}, {'S': '02-08-2020'}, {'S': 
'02-09-2020'}, {'S': '02-10-2020'}, {'S': '02-11-2020'}, {'S': '02-12-2020'}, {'S': '02-01-2021'}, {'S': '02-02-2021'}]}, 'favourites': {'L': [{'N': '83'}, {'N': '93'}, {'N': '162'}, {'N': '105'}, {'N': '137'}, {'N': '86'}, {'N': '98'}, {'N': '95'}, {'N': '114'}, {'N': '153'}, {'N': '79'}, {'N': '119'}]}, 'favourite_count': {'N': '1385'}, 'hashtag_2_percentage': {'S': '95%'}, 'random_tweet_friends': {'N': '353'}, 'statuses': {'N': '240'}}

function deserialise(data){
    const modified_dict = {}
    for (const [key, value] of Object.entries(data)) {
        let modified = Object.values(value)[0]
        if (typeof modified === 'string') {
            modified_dict[key] = modified
        } else {
            modified = modified.map(item => Object.values(item)[0])
        }modified_dict[key] = modified 
    } 
    return modified_dict
}

// templating functions
var dbData = deserialise(data)

// gernerating body from template
var templateScript = Handlebars.templates.index(dbData)

//Rendering index template to body and invoking chart JS graphs

// 
let appendBody = async () => {
  $('#container').append(templateScript)
}

let invokeCharts = () => {
  invokeChart()
  invokeAreaChart(dbData.favourites, 'Favourites by month');
}

$(document).ready(function() {
  appendBody()
  .then(invokeCharts())
})

// window.onload = function(){
//   invokeChart()
//   invokeAreaChart(dbData.favourites, 'Favourites by month');
// }


// Functions to refresh and update dashboard, between retweets and favourites with drop down.
function updateDashboardFavourites() {
    window.myAreaChart.destroy()
    invokeAreaChart(dbData.favourites, 'Favourites by month');
    document.getElementById("charttitle").innerHTML = "Favourites by month";
  }
  
  function updateDashboardRetweets() {
    window.myAreaChart.destroy()
    invokeAreaChart(dbData.retweets, 'Retweets by month');
    document.getElementById("charttitle").innerHTML = "Retweets by month";
  }



