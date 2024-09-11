const config={
    cognito:{
        identityPoolId:"us-west-2_Tawl1HEdD", // put your AWS Cognito Identity Pool ID here (dummy value)
        cognitoDomain:"hotel.auth.us-west-2.amazoncognito.com", // put your AWS Cognito domain here i.e., hote.mydomain.com (dummy value)
        appId:"36mbo3cp0rs3vmg6gbds39rom6" // Create an Applicaiton in AWS Cognito (under User Pool) and put its ID here (dummy value).
    }
}

var cognitoApp={
    auth:{},
    Init: function()
    {

        var authData = {
            ClientId : config.cognito.appId,
            AppWebDomain : config.cognito.cognitoDomain,
            TokenScopesArray : ['email', 'openid'],
            RedirectUriSignIn : 'https://localhost:5000/',
            RedirectUriSignOut : 'https://localhost:5000/',
            UserPoolId : config.cognito.identityPoolId, 
            AdvancedSecurityDataCollectionFlag : false,
                Storage: null
        };

        cognitoApp.auth = new AmazonCognitoIdentity.CognitoAuth(authData);
        cognitoApp.auth.userhandler = {
            onSuccess: function(result) {
              
            },
            onFailure: function(err) {
            }
        };
    }
}