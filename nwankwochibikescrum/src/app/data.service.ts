import {Injectable, OnInit} from '@angular/core';
import {User} from "./user";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Router} from "@angular/router";
import * as jwt_decode from "jwt-decode";
import {CookieService} from "ngx-cookie-service";
import {Goal} from "./goal";
import {Project} from "./project";

@Injectable({
  providedIn: 'root'
})
export class DataService implements OnInit{
  public user: User;
  public user_for_selected_project:User;
  public user_array: any;
  public new_project: Project;
  public goal: Goal;
  public projects;
  public project_owner;
  public allProjects: any;
  public errorMessage;
  public successMessage;
  public redirect;
  public link;
  public confirmPassword: string;
  public isLoggedIn: boolean = false;
  public allUsers: User[] = [];
  public statusList;
  private http: HttpClient;
  private cookie: CookieService;
  private is_projected_selected:boolean = false;
  public is_project_owner:boolean = false;

  private httpOtions = {
    headers : new HttpHeaders({
      'Content-Type': 'Application/json',
      'Authorization': 'Token '+ this._cookie.get('user_token')
    })
  }

  userTypes = ['Owner', 'User'];

  constructor(private _http: HttpClient, private _user: User, private _project:Project, private router: Router, private _cookie: CookieService) {
    this.user = _user;
    this.new_project = this._project
    this.http = _http;
    this.cookie = this._cookie;
    this.cookie.get('token');
    this.getAllProjects();

    // this.checkLoggedInState();
    this.user_for_selected_project = new User()
  }

  ngOnInit(){
    if(this.cookie.check('project_id')){
      this.chooseProject(this.cookie.get('project_name'), this.cookie.get('project_name'))
    }else{
      this.is_projected_selected = false;
    }
  }

  create(){
    const url = "/nwankwochibikescrumy/api/scrumusers/";
    if(this.confirmPassword == this.user.password){
        this.http.post(url, this.user).subscribe(
          data => {
            console.log(data)
            this.successMessage = "your account was created successfully";
            this.redirect = "/login";
            this.link = "go to login";
            this.router.navigateByUrl("success");
          },
          error1 => {
            console.log(error1)
            this.errorMessage = error1.statusText;
            this.redirect = "/signup";
            this.link = "try again";
            this.router.navigateByUrl("error");
          },
          ()=> console.log('completed')
        );
    }
  }

  login(){
    // let credentials = encodeURI(this.user.username+":"+this.user.password)
    // let base64_credentials = btoa(credentials)
    // this.httpOtions.headers.append("Authorization", "Basic " + btoa(this.user.username+":"+this.user.password));


    const url2 = "nwankwochibikescrumy/api-token-auth/"
    let httpOtions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
      })
    }

    let body = {
      user:{
        username: this.user.username,
        password: this.user.password,
      },

      project_id: this.user.login_project_id
    }

    this.http.post(url2, body, httpOtions_).subscribe(
      data => {
        console.log("******^^^^^^^")
        console.log(data);

        // let access_token = data['access'];
        // let refresh_token = data['refresh'];

        // let data = jwt_decode(access_token)
        // this.projects = accessDecode['projects']


        // this.cookie.set('access_token', access_token);
        // this.cookie.set('refresh_token', refresh_token);

        this.cookie.set('first_name', data['first_name']);
        this.cookie.set('last_name', data['last_name']);
        this.cookie.set('username', data['username']);
        this.cookie.set('id', data['id']);
        this.cookie.set('role', data['role']);
        this.cookie.set('token', data['token'])

        if(this.user.login_project_id)
          this.cookie.set('project_id', this.user.login_project_id)

        console.log("done setting cookie")
        console.log(this.cookie.get('username'))

        this.getProjectsList()
        // location.reload()
        // console.log(typeof accessDecode['projects'], accessDecode['projects'][0])
        },
      error1 => {
        console.log(error1);
        this.errorMessage = error1.error.detail;
        this.redirect = "/login";
        this.link = "go to login";
        this.router.navigateByUrl("error");
      },
      () => {
        this.isLoggedIn = this.checkLoggedInState();
        console.log("login_project_id", this.user.login_project_id)

        //After logging in create the user
        this.createUser();

        //get projects list for logged in user
        this.getProjectsList()

        if(this.user.login_project_id) {
          //get all users for project
          this.setUsers();
          this.router.navigateByUrl("blank");
        } else {
          this.route("/blank")
        }
      }
    );
  }

  is_project_in_project_list(){
    let is_in_project = false

    for(let project of this.user.projects){
      console.log(project.name, this.user.login_project_id)
      if(project.name == this.user.login_project_id){
        is_in_project = true
        this.cookie.set("project_name", project.name)
      }
    }

    if(!is_in_project){
      console.log("ADDING USER TO THE PROJECT")
      this.addUserToProject()
      // this.route("/scrumboard")
    }

    return is_in_project
  }

  private addUserToProject() {
    // console.log("getProjectsList")
    const url = "/nwankwochibikescrumy/api/scrumusers/" + this.cookie.get('id') + "/add-user-project/"
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    };

    this._http.post(url, {"project_id": this.user.login_project_id}, httpOptions_).subscribe(
      data => {
        console.log("data from get all Projects", data)
        this.allProjects = data;
      },
      error1 => console.log(error1),
      () => {
        console.log("dunno why I commented this out")
        // this.route('/all-tasks')
      }
    )
  }


  logout(){
    this.cookie.deleteAll();
    localStorage.clear();
    this.checkLoggedInState();
    this.createUser();
    this.route("/login")
  }

  checkLoggedInState(){
    // console.log("checkLoggedInState")
    return this.cookie.check('token')
  }

  createUser(){
    if (this.checkLoggedInState()){
      this.user.firstname = this.cookie.get('first_name');
      this.user.lastname = this.cookie.get('last_name');
      this.user.username = this.cookie.get('username');
      this.user.role = this.cookie.get('role')
      this.user.projects = this.projects
      this.user.current_project = this.cookie.get('project_name')
      console.log("create user")
      console.log()
    }
  }

  getUser(){
    console.log("get user goals MMMM")
    const url = "nwankwochibikescrumy/api/users/" + this.cookie.get('project_id') + "/user-goals/?user_id=" + this.cookie.get('username');
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    };

    this._http.get(url, httpOptions_).subscribe(
      (data) => {
        let user = data["user"]
          let newUser = new User();

          newUser.id = user['id']
          newUser.firstname = user['first_name']
          newUser.lastname = user['last_name']
          newUser.username = user['username']
          newUser.goals = user['goals']
          newUser.projects = user['project_set']

          this.user_for_selected_project = newUser
          this.user_array = [newUser]
          // this.user_array.push(newUser)

      },
      error1 => console.log(error1),
      () => {
        console.log("complete projects retrieval for get user goals MMM: ", this.user_array)

        // this.cookie.set("project_id", project_id)
        // this.cookie.set("project_name", project_name)
        // this.user.current_project = project_name;
        // this.is_projected_selected = true
        // this.getProjectsList()
        // this.route("all-tasks")
      }
    )
  }

  //gets all users of a project
  setUsers(){
    console.log("token before call: ", this.cookie.get('token'))
    let httpOtions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    }
    // this.cookie.check('project_name')
    if(true){
        // alert("wow")
        const url = "/nwankwochibikescrumy/api/users/" + this.cookie.get('project_id') + "/projects-users/";
        this.http.get(url, httpOtions_).subscribe(
        (data) => {
          let x : User[] = data["users"].map(user => {
            let newUser = new User();

            newUser.id = user['id']
            newUser.firstname = user['first_name']
            newUser.lastname = user['last_name']
            newUser.username = user['username']
            newUser.goals = user['goals']
            newUser.role = user['groups'][0]['name']
            newUser.projects = user['project_set']



            return newUser;
          });

          alert("auth_user"+ data["auth_user"])
          this.project_owner = data["project_owner"]
          this.cookie.set('project_owner', this.project_owner)
          this.cookie.set("user_project_role", data["user_role_id"])
          this.cookie.set("user_role_name", data["user_role_name"])
          this.cookie.set("auth_user", data["auth_user"])

          if(this.cookie.get('username') == this.project_owner)
            this.is_project_owner = true;
          this.allUsers = x;
        },
        error1 => console.log(error1),
        () => {
          console.log("complete")
          console.log(this.allUsers)
        }
      )
    }else{
      // alert("I am not supposed to be here")
      console.log("going to blank from setUsers")
      this.route('blank')
    }
    return this.allUsers;
  }

  private getToken() {
    let now = Date.now();
    let access_token = this.cookie.get('access_token')
    let refresh_token = this.cookie.get('refresh_token')

    console.log("in get token fresh")
    if(access_token != "" && refresh_token != "") {
      console.log("there are tokens in our cookies")
      console.log(typeof access_token)
      let access_expiry_date = this.getExpiryDate(this.cookie.get('access_token'))
      let refresh_expiry_date = this.getExpiryDate(this.cookie.get('refresh_token'))

      let current_access_token = new Date(access_expiry_date * 1000)
      let current_refresh_token = new Date(refresh_expiry_date * 1000)

      if (current_refresh_token.getTime() > now) {
        if (current_access_token.getTime() > now) {
          console.log("access_token has not expired" + current_access_token.getTime(), current_refresh_token.getTime(), now)
          return this.cookie.get('access_token')
        } else {
          console.log("in get new token")
          return this.getNewToken();
        }
      } else {
        console.log("r: " + parseInt(this.cookie.get('access_token')) + ", now: " + now)
        console.log("refresh_token HAS expired")
        this.logout()
        return "";
      }
    }

    if (refresh_token == "")
      this.logout()
  }

  private getExpiryDate(token: string) {
    let decoded_token = jwt_decode(token);
    return decoded_token['exp']
  }


  private getNewToken() {
    let new_token = ""
    const url = "/nwankwochibikescrumy/api-token-auth/refresh/";

    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
      })
    }

    this.http.post(url,{'refresh': this.cookie.get('refresh_token')}, httpOptions_).subscribe(
      data => {
        new_token = data['access']
        console.log("about to set the new token")
        this.cookie.set('access_token', new_token)
        this.route("")
      },
      error1 => console.log(error1),
      () => {
        return new_token;
      }
    )

    console.log("returning the new token")

  }

  hostName = "http://localhost:4200/";

  getStatusList(){
    const url = "/nwankwochibikescrumy/api/status/";

    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    }

    this.http.get(url, httpOptions_).subscribe(
      (data:[]) => {
        let statusList = data.map(status => {
          let statusObj = {}
          statusObj[status['id']] = status['status_name']
          statusObj['id'] = status['id'];
          statusObj['status_name'] = status['status_name'];
          return statusObj;
        });

        this.statusList = statusList;
      }
    )
  }

  getAllProjects(){
    console.log("getProjectsList")
    console.log("token before call: ", this.cookie.get('token'))
    const url = "nwankwochibikescrumy/api/projects/"
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        // 'Authorization': 'Token  ' + this.cookie.get('token
      })
    };

    this._http.get(url, httpOptions_).subscribe(
      data => {
        console.log("data from get all Projects", data)
        this.allProjects = data;
      },
      error1 => console.log(error1),
      () => console.log("complete ALL projects retrieval")
    )
  }

  //get the projects of a particular user
  getProjectsList(){
    console.log("getProjectsList")
    const url = "nwankwochibikescrumy/api/scrumusers/" + this.cookie.get('id') + "/user-projects/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    };

    this._http.get(url, httpOptions_).subscribe(
      data => {
        console.log("data from getProject", data)
        this.user.projects = data;
      },
      error1 => console.log(error1),
      () => {
        console.log("complete projects retrieval")
        //check if user is in login_project_id
        // this.is_project_in_project_list()
      }

    )
  }

  chooseProject(project_id, project_name){
    console.log("chooseProjectsList")
    console.log("token before call: ", this.cookie.get('token'))
    const url = "nwankwochibikescrumy/api/users/" + project_id + "/projects-users/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    };

    this._http.get(url, httpOptions_).subscribe(
      (data: User[]) => {
        let x : User[] = data["users"].map(user => {
          let newUser = new User();

          newUser.id = user['id']
          newUser.firstname = user['first_name']
          newUser.lastname = user['last_name']
          newUser.username = user['username']
          newUser.goals = user['goals']
          newUser.projects = user['project_set']

          return newUser;
        });

        this.project_owner = data["project_owner"]
        this.cookie.set('project_owner', this.project_owner)
        this.cookie.set("user_project_role", data["user_role_id"])
        this.cookie.set("user_role_name", data["user_role_name"])
        this.cookie.set("auth_user", data["auth_user"])

        if(this.cookie.get('username') == this.project_owner){
          this.is_project_owner = true
          // alert(this.cookie.get('username') == this.project_owner)
        } else {
          this.is_project_owner = false
        }



        this.allUsers = x;
      },
      error1 => console.log(error1),
      () => {
        console.log("complete projects retrieval for choose projects: ", this.allUsers)

        this.cookie.set("project_id", project_id)
        this.cookie.set("project_name", project_name)
        this.user.current_project = project_name;
        this.is_projected_selected = true
        this.getProjectsList()
        this.route("all-tasks")
      }
    )
  }

  createNewGoal(){
    const url = "/nwankwochibikescrumy/api/scrumgoals/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    }
    this.goal.project_name = this.user.current_project
    this.http.post(url, this.goal, httpOptions_).subscribe(
      data => {
        console.log(data)
        this.successMessage = "New goal was successfully created";
        this.redirect = "/scrumboard";
        this.link = "back to scrumboard"
        this.router.navigateByUrl("success");
      },
      error1 => {
        console.log(error1);
        this.errorMessage = error1.statusText;
        this.redirect = "/add-goal";
        this.link = "back to goal creation form"
        this.router.navigateByUrl("error");
      },
      () => {
        console.log('completedx')
        this.setUsers()
      }
    );
  }

  deleteGoal(id: number, goal_random_id:number){
    alert("this goal with id: "+ goal_random_id +" has been deleted.")
    const url = "/nwankwochibikescrumy/api/scrumgoals/" + id + "/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token')
      })
    };
    this.http.delete(url, httpOptions_).subscribe(
      data => console.log(data),
      error1 => console.log(error1.statusText),
      () => {
        this.route("scrumboard")
      }
    );
  }


  moveGoal(goal_id: any, move_id){
    const url = "/nwankwochibikescrumy/api/scrumgoals/" + goal_id + "/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token'),
        'custom-mode': 'move'
      })
    };

    this._http.patch(url, {"goal_status":move_id}, httpOptions_, ).subscribe(
      data =>{
        console.log(data)
        this.getProjectsList()
      },
      error1 => console.log(error1),
      () => {
        // this.route("scrumboard")
      }
    )

  }

  is_logged_in_user_project_owner(){
    // alert("username: "+ this.project_owner)
    if(this.cookie.get('username') == this.project_owner)
      return true
    return false
  }

  changeGoalOwner(goal_id, new_owner, status_id){
    const url = "/nwankwochibikescrumy/api/scrumgoals/" + goal_id + "/"
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token'),
        'custom-mode': 'change_owner'
      })
    };

    this._http.put(url, {"user_id":new_owner, "status_id": status_id}, httpOptions_).subscribe(
      data => {
        console.log(data)
      },
      error1 => {
        console.log(error1)
      },
      () => {
        console.log("completed")
        // this.route("")
      }
    )
  }

  editGoalText(goal_id: any, goal_text){
    const url = "/nwankwochibikescrumy/api/scrumgoals/" + goal_id + "/";
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token ' + this.cookie.get('token'),
        'custom-mode': 'edit_goal_name'
      })
    };

    this._http.put(url, {"goal_name":goal_text}, httpOptions_, ).subscribe(
      data => console.log(data),
      error1 => console.log(error1),
      () => {
        this.route("")
      }
    )
  }

  createNewProject(){
    console.log("create new project")
    const url = "nwankwochibikescrumy/api/scrumprojects/"
    let httpOptions_ = {
      headers : new HttpHeaders({
        'Content-Type': 'Application/json',
        'Authorization': 'Token  ' + this.cookie.get('token')
      })
    };

    this._http.post(url,
      {
        'name':this.new_project.name,
        "user_id": this.cookie.get('id')
      },
      httpOptions_)
      .subscribe(
      data => {
        console.log("new project", data)
        this.getProjectsList()
      },
      error1 => console.log(error1),
      () => {
        console.log("project create completed")
        this.route("")
      }
    )
  }

  route(routeName: string){
    this.router.navigateByUrl(routeName)
  }

  enableActive(event){
    let navBtn = document.getElementsByClassName("nav-btns")
    // for(item of navBtn){
    //
    // }
  }

  parseJwt (data) {
    console.log("in parseJwt")
    console.log(data)
    let token = data['access'];
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    let jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};


}

