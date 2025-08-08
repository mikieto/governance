package gov.law.style
import rego.v1

deny[msg] if {
  input.kind == "content"
  re_match(`\b(latest|最近|直近|今年)\b`, input.content)
  msg := "Relative time is banned; use YYYY-MM-DD."
}
