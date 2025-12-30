output "load_balancer_ip" {
  description = "The public URL for the application load balancer."
  value = "https://${aws_lb.alb.dns_name}"
}