import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginformComponent} from "./loginform/loginform.component";
import {RegisterFormComponent} from "./register-form/register-form.component";
import {HomeComponent} from "./home/home.component";
import {WelcomeComponent} from "./welcome/welcome.component";
import {ScrumboardComponent} from './scrumboard/scrumboard.component';
import {AddGoalsComponent} from "./add-goals/add-goals.component";
import {ErrorComponent} from "./error/error.component";
import {SuccessComponent} from "./success/success.component";
import {ChangeOwnerFormComponent} from "./change-owner-form/change-owner-form.component";
import {AllTaskBoardComponent} from "./all-task-board/all-task-board.component";
import {BlankProjectComponent} from "./blank-project-component/blank-project.component";
import {NewProjectComponent} from "./new-project/new-project.component";
import {ChangeRoleComponent} from "./change-role/change-role.component";


const routes: Routes = [
  {path:'', component:HomeComponent},
  {path:'welcome', component:WelcomeComponent},
  {path:'scrumboard', component:ScrumboardComponent},
  {path:'all-tasks', component:AllTaskBoardComponent},
  {path:'add-goal', component:AddGoalsComponent},
  {path:'login', component:LoginformComponent},
  {path:'signup', component:RegisterFormComponent},
  {path:'change-owner/:goal_id', component:ChangeOwnerFormComponent},
  {path:'error', component:ErrorComponent},
  {path:'success', component:SuccessComponent},
  {path:'blank', component:BlankProjectComponent},
  {path:'new-project', component:NewProjectComponent},
  {path:'change-role', component:ChangeRoleComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [
  LoginformComponent,
  RegisterFormComponent,
  ChangeOwnerFormComponent,
  HomeComponent,
  WelcomeComponent,
  ScrumboardComponent,
  AddGoalsComponent,
  ErrorComponent,
  SuccessComponent,
  AllTaskBoardComponent,
  BlankProjectComponent,
  NewProjectComponent,
  ChangeRoleComponent
]
