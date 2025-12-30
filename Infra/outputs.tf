output "load_balancer_ip" {
  description = "The public URL for the application load balancer."
  value = "https://${aws_lb.my_lb.dns_name}"
}