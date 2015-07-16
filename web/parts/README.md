### 编写Part注意事项 ###
> 标准结构

	<!-- Start Comment -->
	<div class="magic-name" id="your-magic-name-id">
	    <i class="icon-check-empty icon-large"></i>Magic Name
	</div>
	<div class="magic-mirror" id="your-magic-mirror-id">
	    <!-- Content -->
	</div>
	<script type="text/javascript">
		<!-- Your Scripts -->
	</script>
	<!-- End Comment-->

window.iframe_register: 注册你的脚本，脚本会在所有Part加载完毕后立即执行  
Magic(magicName, wizardName, index, incantation): 魔法对象，对应一个操作

*magicName: 魔法名称，当前操作名称*  
*wizardName: 魔棒名称，当前流程名称（整个场景请保持一致）*  
*index: 执行序列*  
*incantation: 咒语，操作主函数（在执行Magician.fire时，按index执行此函数）*  

Magician.practice(magic): 训练魔法，将魔法附加到魔棒

*magic: 魔法对象*  
 
magic.ready: 魔法是否准备完毕，当前魔法准备完毕以保证下一个魔法继续进行  

Magician.fire(wizardName, initData): 施放魔法，尝试检查整个魔法序列

*wizardName: 魔棒名称*  
*initData: 初始数据*

{{key}}: 替换规则  
\_\_\_key\_\_\_: 替换规则  