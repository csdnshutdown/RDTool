import numpy as np
import matplotlib.pyplot as plt


# init plot
class MatPlotbyPci:
    def __init__(self):
        # 准备好角度
        self.omega = 2 * np.pi
        self.CUR_POS = lambda member, sum : member/sum*self.omega/2
        self.CUR_SCALE = lambda member, sum : member/sum*self.omega
        self.fig = plt.figure('param by pci', figsize = (10,100))

    def remove_inv_pci(self, i, pci_value, duration_value, y_value_value):
        if i < 0:
            return pci_value, duration_value,y_value_value
        else:
            if "/" in pci_value[i]:
                pci_value.pop(i)
                duration_value.pop(i)
                y_value_value.pop(i)
            return self.remove_inv_pci(i-1, pci_value, duration_value, y_value_value)

    def gen_polar_plot(self, duration, pci, y_value, cnt):
        pre_total_scale = 0
        duration_value = duration[1:]
        y_value_label = y_value[0]
        y_value_value = y_value[1:]
        pci_value = pci[1:]
        # 全部输出
        axes = self.fig.add_subplot(50,1,cnt, polar = False)
        pci_value, duration_value, y_value_value = self.remove_inv_pci(len(pci_value)-1, pci_value, duration_value,y_value_value)
        for i in range(len(pci_value)):
            if ' /' in pci_value[i]:
                pci_value.pop()
                duration_value,pop(i)
                y_value_value.pop(i)

        # 判输出参数，只选取部分参数进行输出
        if "TPUT" in y_value_label:
            for i in range(len(y_value_value)):
                y_value_value[i] = y_value_value[i]/1000000

        #绘制总的加权均值：
        avg_weight_tput = np.average(y_value_value, weights = duration_value)
        plt.bar(self.omega/2, avg_weight_tput, width = self.omega, color = "white",edgecolor = "red", align = "center")
        plt.text(0, avg_weigth_tput, 'avg:%.2f'%avg_weight_tput, ha='center', va='center',fontsize=5, c='black', weight='semibold')

        x_axis_pos = []
        x_axis_dur = []
        y_axis_center = []
        for i in range(len(duration_value)):
            if ' /' in pci_value[i]:
                continue
            cur_center = pre_total_scale + self.CUR_SCALE(duration[i], sum(duration_value))/2
            y_value_value[i] = round(y_value_value[i],2)
            plt.bar(
                pre_total_scale + self.CUR_POS(duration_value[i], sum(duration_value)),# 上次扇面角度＋当前扇面角度/2
                y_value_value[i], # 当前pci的value值， 取整数
                width = self.CUR_SCALE(duration_value[i], sum(duration_value)), # 当前pci的弧度，取决于在该PCI的时间
                alpha = 0.65 # 设置为半透明，以便总体甲醛平均的图形可以显示出来
            )
            y_axis_center.append(cur_center)
            pre_total_scale += self.CUR_SCALE(duration_value[i], sum(duration_value))

            # x轴标签设置
            x_axis_pos.append(pre_total_scale)
            x_axis_dur.append("%s:" %pci_value[i]
                              + str(
                                    int(
                                        sum(duration_value) * pre_total_scale/self.omega
                                        )
                                    ) +'s'
                            )
            # 添加y轴标签：
            for a,b in zip(y_axis_center, y_value_value):
                if b < avg_weight_tput: # 大于平均速度的显示绿色，小于的显示红色
                    plt.text(a,b,b, ha='center', va='center', fontsize=5, c='red', weigth='semibold')
                else:
                    plt.text(a,b,b, ha='center', va='center', fontsize=5, c='green', weigth='semibold')

            # 添加y轴标签,替换极坐标角度，并将x轴标签客制化为和实际的tput时长相匹配的秒数：
            plt.xticks(x_axis_pos, x_axis_dur, font=5, rotation=60)
            # y轴标签字体
            plt.yticks(fontproperties='Times New Roman',fontsize=5)
            # 添加title
            plt.title("%s by PCI\n(weighted avg:%.2f" %(y_value_label, avg_weight_tput),fontsize=6, weight='bold', loc='center')
            # plt.subplot(2,2,1)

        def output_polar_plot(self, filename):
            self.fig.tight_layout()
            plt.savefig(filename) # 保存图片
            # plt.show()

#数据准备
if __name__ == "__main__":
    tput = ['tput', 72,55,224,541]
    duration_value = ['time_dur', 23,44,63,14]
    pci = ["PCI:23","PCI:345","PCI:12","PCI:85"]
    mat_inst = MatPlotbyPci()
    mat_inst.gen_polar_plot(duration_value,pci,tput)
    mat_inst.output_polar_plot()