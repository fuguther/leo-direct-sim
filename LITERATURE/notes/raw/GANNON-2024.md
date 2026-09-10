# Continuous Spacecraft Communications via Make-Before-Break Antenna Array Beam Steering (GANNON-2024)

它解决一个工程痛点:航天器在 GEO 中继视线边缘时通信中断,用有源相控阵双波束 make-before-break 切换保无隙连续通信。证据链较完整:商用终端特性数据→仿真(LEO→GEO,Ka 段,均值 3 Mbps、最差切换还有 0.8 Mbps)→硬件原型暗室+OTA 双中继切换实测(切换中遥测无误码)。舒服之处:少数既有仿真又有硬件实测的工作。边界:面向 LEO-GEO 中继,不是 LEO-ISL;波束数、切换时序由硬件决定,算法层面收益有限。保留"该工作表明设备级 GSL 切换可无间隙"这一论文启示。但注意这是设备级波束分切,与星座级路由的链路生命周期不是一层,别过度引申。无公开代码(硬件工作,未核实)。

> 状态: 摘要；未核实字段: 终端型号与切换时序细节、仿真参数、公开代码
