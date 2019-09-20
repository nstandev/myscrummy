import { Component, OnInit } from '@angular/core';
import {DataService} from "../data.service";
import {DragulaService} from "ng2-dragula";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-all-task-board',
  templateUrl: './all-task-board.component.html',
  styleUrls: ['./all-task-board.component.css']
})
export class AllTaskBoardComponent implements OnInit {
  public dataService: DataService
  public sub: Subscription
  private goalToMove;

  constructor(private _dataService:DataService, private _dragula: DragulaService) {
    this.dataService = this._dataService

     this.sub = this._dragula.drop().subscribe(value => {
      console.log(value)
      console.log(value.target.id)
       console.log(value.source.className)
      console.log(value.target.attributes)
      if (value.target.id == "remove"){
        // this._dataService.deleteGoal(this.goalToMove["id"], this.goalToMove["goal_id"])
      } else{
        // this._dataService.moveGoal(this.goalToMove["id"], value.target.id)
      }
    })

    this._dragula.createGroup("GOAL", {
      moves: (el, source, handle, sibling) => {
        console.log("MOVE")
        console.log(source.className)
        return source.className == 'Owner'
      }
    })
  }

  ngOnInit() {
    console.log("inside all task init")
    this._dataService.setUsers();
    this._dataService.getStatusList();
    this._dataService.getProjectsList()
  }

  setGoalIDToMove(goal){
    console.log(goal)
    this.goalToMove = goal;
  }

  onTableClick(event){
    let target_parent = event.target.parentNode
    console.log(target_parent)
    if (event.target.parentNode.classList.contains("task-div")){
      let text = target_parent.getElementsByClassName("goal-text").item(0).innerText
      // this.editGoalText(prompt("Edit goal", text));
    }
  }


  ngOnDestroy(): void {
    // this._subscription.unsubscribe()
    this.sub.unsubscribe()
  }
}
