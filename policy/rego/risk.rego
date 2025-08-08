package gov.law.risk
import rego.v1

deny[msg] if {
  input.kind == "task"
  input.risk == "HIGH"
  input.approval != "pr"
  msg := sprintf("HIGH risk requires approval=pr: %s", [input.id])
}
