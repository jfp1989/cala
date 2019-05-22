export FN_AUTH_REDIRECT_URI=http://localhost:8040/google/auth
export FN_BASE_URI=http://localhost:8040
export FN_CLIENT_ID=856719457835-qft94hdq52mo9re6vo234hml7m4affa5.apps.googleusercontent.com
export FN_CLIENT_SECRET=20S4G-hgk6Cl1A9o9VCUGAxt

export FLASK_APP=kapp:app
export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY=hgk6Cl1A9o9VCUGAxt



export GOOGLE_LOGIN_CLIENT_ID=856719457835-qft94hdq52mo9re6vo234hml7m4affa5.apps.googleusercontent.com
export GOOGLE_LOGIN_CLIENT_SECRET=20S4G-hgk6Cl1A9o9VCUGAxt
declare OAUTH_CREDENTIALS
OAUTH_CREDENTIALS=( ['id']:'856719457835-qft94hdq52mo9re6vo234hml7m4affa5.apps.googleusercontent.com' ['secret']='20S4G-hgk6Cl1A9o9VCUGAxt')


python3 -m flask run -p 8040