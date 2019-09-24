import { Component, OnInit } from '@angular/core';
import {DataService} from "../data.service";

@Component({
  selector: 'app-change-role',
  templateUrl: './change-role.component.html',
  styleUrls: ['./change-role.component.css']
})
export class ChangeRoleComponent implements OnInit {
  public user_id
  public group_id

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.setUsers()
    this.dataService.getRoles()
  }

  changeUserRole() {
    this.dataService.changeUserRole(this.user_id, this.group_id)
  }
}
