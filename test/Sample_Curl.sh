#*******SignUp *********
echo "Sign Up"
curl -i -H "Content-Type:application/json" -X POST -d '{"firstName":"Tom","lastName":"Jerry","email":"tom_jerry@gmail.com","password":"tomjerry"}' http://localhost:8080/users/reg

#*******Sing In ******
echo "Sign In"
curl -i -H "Content-Type:application/json" -X POST -d '{"email":"tom_jerry@gmail.com","password":"tomjerry"}' http://localhost:8080/users/login

#****** Create Board *****
echo "Create Board"
curl -i -H "Content-Type:application/json" -X POST -d '{"boardName":"Clark_Hall","boardDesc":"IPS","privacy":"False"}' http://localhost:8080/users/4/boards

#***** Get User Board ******
echo "Get User Board"
 curl -i -H "Content-Type:application/json" -X GET  http://localhost:8080/users/4/boards

#*******Get all boards ****** 
echo "Get All Boards"
curl -i -H "Content-Type:application/json" -X GET  http://localhost:8080/users/13/allboards

#****** Create Pin *********
echo "Create Pin"
curl -i -H "Content-Type:application/json" -X POST -d '{"pinName":"NewPin","description":"test"}' http://localhost:8080/users/4/boards/Clark_Hall/pins


#****** View Pin *******
echo "View Pin"
curl -i -H "Content-Type:application/json" -X GET   http://localhost:8080/users/4/boards/Clark_Hall/pins/2

#***** Create Comment ****
echo "Create Comment"
curl -i -H "Content-Type:application/json" -X POST -d '{"description":"Amazing"}' http://localhost:8080/users/4/boards/Clark_Hall/pins/2/comment

#******** Update Comment *****
echo "Update Comment"
curl -i -H "Content-Type:application/json" -X PUT -d '{"description":"New Amazing"}' http://localhost:8080/users/4/boards/Clark_Hall/pins/2/comment/3

#******** Delete Comment *****
echo "Delete Comment"
curl -i -H "Content-Type:application/json" -X DELETE http://localhost:8080/users/4/boards/Clark_Hall/pins/2/comment/3

