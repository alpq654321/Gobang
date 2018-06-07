username = "";
username2 = "";
passwork = ""; //存储密码 (password不能用……)
Store = []; //存储用户信息
sum = 1;
turn = 0;
Query = 0;
Last = 0;
var SUBMIT = false;
function centerIt(x, delta)
{
	var midWidth = parseInt($('#img').css('height')) >> 2;
	var midHeight = document.body.clientWidth >> 1;
	x.css('top', midWidth + delta);
	x.css('left', midHeight - (((parseInt(x.css('width'))) >> 1) + parseInt(x.css('padding-left'))));
}
centerIt($('#welcome2'), -380);
centerIt($('#choose'), -180);
centerIt($('#welcome'), -280);
centerIt($('#username'), -50);
centerIt($('#password'), 50);
centerIt($('#register'), 180);
centerIt($('#submit'), 180);
centerIt($('#draftsDashboard'), -30);
var midHeight = document.body.clientWidth >> 1;
$('#register').css('left', midHeight - 350);
$('#submit').css('left', midHeight + 150);
function showIt(x) 
{
	var det = parseInt(x.css('height')) >> 2;
	x.css('top', (parseInt(x.css('top'))) - det);
	x.css('display', 'block');
	x.animate({'top':'+=' + det.toString(), 'opacity':'+=1'}, 1000);
}
setTimeout("showIt($('#welcome'))", 1000);
setTimeout("showIt($('#username'))", 2000);
setTimeout("showIt($('#password'))", 2000);
setTimeout("showIt($('#register'))", 3000);
setTimeout("showIt($('#submit'))", 3000);

$(function(){
    $("#submit").click(function() { //点击登录时
		username=$("#username_text").val();
		passwork=$("#password_text").val();
		$.ajax({  
                    type:"POST",  
					url:"/submit",
                    data:{"username":username, "password":passwork},  
                    dataType:"json",  
                    success:function(data){  
						if (data==="ojbk") //登录成功
						{
							Store[0]=username;
							username2=username;
							SUBMIT = true;
							$('#welcome').fadeOut();
							$('#username').fadeOut();
							$('#password').fadeOut();
							$('#register').fadeOut();
							$('#submit').fadeOut();
							setTimeout("showIt($('#welcome2'))", 1000);
							setTimeout("showIt($('#choose'))", 2000);
							setTimeout("showIt($('#draftsDashboard'))", 3000);
							
						}
						else alert(data); //登录失败
                    },  
                    error:function(XMLHttpRequest, textStatus, errorThrown) {  
                            alert(XMLHttpRequest.status);  
                            alert(XMLHttpRequest.readyState);  
                            alert(textStatus);  
                        }  
      });  
    });
    $("#register").click(function() { //点击注册时
		var username=$("#username_text").val();
		var passwork=$("#password_text").val();
		$.ajax({  
                    type:"POST",  
					url:"/register",
                    data:{"username":username, "password":passwork},  
                    dataType:"json",  
                    success:function(data){  
                       alert(data);   //返回是否注册成功
                    },  
                    error:function(XMLHttpRequest, textStatus, errorThrown) {  
                            alert(XMLHttpRequest.status);  
                            alert(XMLHttpRequest.readyState);  
                            alert(textStatus);  
                        }  
      });  
    });
})
function Effect(x) //点击邀请按钮时该有的反应
{
	$("#Invite"+x.toString()).click(function() {
								
	$.ajax({  
		type:"POST",  
		url:"/invite",
		data:{"first":username2, "second":Store[x]},  
		dataType:"json",
		success:function(data){ 
		if (data === "NO！！")
			alert("这名玩家正在被别人邀请或者正在邀请别人或者正在激战中，请稍后！"); else
			{
				alert(data);
				Query = 1; //等待对方是否接受邀请
			}
		}
	})
	})
}
 $.ajaxSetup({async:false})
        setInterval('ok()',1000)
        function ok(){
			if (SUBMIT===true) //如果已登录，才需要得到服务器返回的用户列表以及邀请信息
			{
            $.get('/loginInfo',function(data){
                if(data != ''){
                    var userList=data.split(',');
                    for (var i in userList){  //枚举所有用户
                        var userName=userList[i];
						var OK = true;
						for (var j=0; j<sum; j++)
							if (userName===Store[j]) OK=false;
						if (OK === true) //如果这个用户没有出现过
						{
							var TOP = sum * 80 + 40;
							var item="<div class='Name' id ='Name"+sum.toString()+"'style='left:30px; top:"+TOP.toString()+"px; font-size:2em'>"+userName+"</div>"+"<div class='Invite' style='right:30px; top:"+TOP.toString()+"px'id = 'Invite"+sum.toString()+"'>邀请</div>"
							var $drafts= $('#draftsDashboard');
							$drafts.animate({height:'+=80px'}, 500);
							$('#draftsDashboard').append(item);
							Store[sum]=userName;
							
							setTimeout("showIt($('#Name"+sum.toString()+"'))", 1000);
							setTimeout("showIt($('#Invite"+sum.toString()+"'))", 1000);
							sum ++;
						}
                    }
                }
				for (var i=Last; i<sum; i++)
					Effect(i); //给这些新用户增加上邀请按钮
				Last=sum;
			});
            $.get('/inform',function(data){
				var userList=data.split(',');
                for (var i in userList) //枚举所有邀请信息
				{
					if (i%2===1 && userList[i]===username2)  //得到被人的邀请
					{
						console.log(i);
						var userName=userList[i-1];
						if (confirm(userName+'正在邀请你，敢不敢迎战！')){  //选择是否迎战
								
						$.ajax({  //无论是否迎战都报告给服务器，如果迎战则跳出对战界面
							type:"POST",  
							url:"/confirm",
							data:{"first":userName, "second":username2},  
							dataType:"json",
							success:function(data){ 
								alert("打起来了！");
								window.location.href='/white/'+username2+'_'+userName;
							}
						}) 
					}else {
						$.ajax({  
							type:"POST",  
							url:"/refuse",
							data:{"first":userName, "second":username2},  
							dataType:"json",
							success:function(data){ 
							alert("没打起来！");
						}
						})  
					}
					}
                }
			})
			if (Query===1) //如果之前邀请过别人，则需要等待是否迎战
			{
				$.get('/accept/'+username2,function(data){ //得到所有接受的信息
						if (data!="") //如果对方同意，报告给服务器表示我收到了！然后进去对战页面
						{
							var userName=data;
							alert("对方同意了！！");
							$.ajax({  
									type:"POST",  
									url:"/acceptafter",
									data:{"first":username2, "second":userName},  
									dataType:"json",
									success:function(data){ 
										Query = 0;
										window.location.href='/black/'+username2+'_'+userName;
									}
								})
						}
					
				})
				$.get('/wrong',function(data){//得到所有拒绝的信息
					var userList=data.split(',');
                    for (var i in userList)
					{
						if (i%2===0 && userList[i]===username2) //如果对方拒绝，报告给服务器表示我收到了！
						{
							console.log(i);
							var userName=userList[i+1];
							alert("对方拒绝了！！");
							$.ajax({  
									type:"POST",  
									url:"/wrongafter",
									data:{"first":username2, "second":userName},  
									dataType:"json",
									success:function(data){ 
										Query = 0;
									}
								})
							
						}
                    }
				})
			}
			}
		}