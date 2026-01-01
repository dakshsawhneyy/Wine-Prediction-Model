output "Change_Config_Command" {
  value = "az aks get-credentials --resource-group ${azurerm_resource_group.demo.name} --name ${azurerm_kubernetes_cluster.demo.name}"
}