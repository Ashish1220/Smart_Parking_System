const express = require('express');
const app = express();
const User=require('./model.js')
const cookie_parser=require('cookie-parser')
const cors=require('cors')
const tokenizer=require('jsonwebtoken')
app.use(express.urlencoded({ extended: false }));
app.use(express.json())
app.use(cookie_parser())
app.use(cors({
    origin: 'http://localhost:3000', // Adjust with your React app's origin
    credentials: true, // Enable credentials (cookies, authorization headers) cross-origin
  }));
app.post('/register', async (req, res) => {

  try {
    const existingUser = await User.find({
      email: req.body.email
    });
    console.log(req.body.email)
    
    if (existingUser.length!=0) {
      return res.status(400).json({ error: 'User already present' });
    }

    const newUser = new User({
        name: req.body.name,
        email: req.body.email,
        password: req.body.password,
        role:req.body.role,
    });
    
    const savedUser = await newUser.save();

    
    res.status(201).send('Registered');
  } catch (err) {
    console.error('Error creating user:', err);
    res.status(400).json({ error: 'Fill all the feilds ,Error creating user' });
  }
});

app.get('/register',async (req,res)=>{
    all_users=await User.find({})
   res.json({all_users})
})

app.get('/login',(req,res)=>{
    return res.send('login now!');
})

app.post('/login',async (req,res)=>{
    
    console.log('trying to log in');
    if(req.cookies.jwt){
        console.log("cookie is present")
        
        return res.json({'status 200':'s'});
    }

   const email=req.body.email
   console.log(email)
   const db_user=await User.find({email:email})
   if(db_user.length==0){
    return res.json({'err':'user not registered on this email'})
   }
   else{
       let password=req.body.password


    if(password===db_user[0].password){
        console.log(password)
        const token= tokenizer.sign({User_email:req.body.email,User_password:req.body.password},"1234")
        res.cookie("jwt",token)
        return res.json({'status 200':'s'})
    }
    else{
        return res.json({'err':'password invalid'})
    }
   }
})

app.get('/home',  (req,res)=>{
    

    if(req.cookies.jwt){

        
        tokenizer.verify(req.cookies.jwt,'1234',async (err,decoded)=>{

            if(err){
                console.log('jwt token is invalid');
                res.redirect('/login')
            }
            else{
                const db_user=await User.find({email:decoded.User_email});
                if(db_user.length!=0) {return res.json(db_user[0]);}
                else {
                console.log('No such user exist');
                    res.redirect('/login');}
            }
        }
        )
    }
    else{
        console.log('user  not logged in');
        return res.send("ns");
    }
});
app.get('/logout',(req,res)=>{
console.log("logged-out")
    res.clearCookie('jwt');

    return res.send('Logged out successfully');
})

app.get('/admins',(req,res)=>{
    if(req.cookies.jwt){
        tokenizer.verify(req.cookies.jwt,'1234',async (err,decoded)=>{

            if(err){
                res.redirect('/login')
            }
            else{
                const db_user=await User.find({email:decoded.User_email});
                if(db_user[0].role==='ADMIN'){
                return res.send(`WELLCOOMEE TO ADMIN PAGE ${db_user[0]} `);
            }else{
                return res.send(`YOU ARE NOT ALLOWED TO THIS PAGE `);
            }
            }
        }
        )
    }
    else{
        return res.redirect('/login');
    }

})

// app.post('/add_expense',(req,res)=>{
//     if(req.cookies.jwt){
//         console.log("in")
//         const db_user=tokenizer.verify(req.cookies.jwt,'1234',async (err,decoded)=>{
//             if(err){
//                 console.log('Invalid cookie please sign in again');
//             }
//             else{

//                 let db_user=await User.find({email:decoded.User_email})
//                 const temp_exp=db_user[0].current_funds

//                 console.log(req.body);
//                 if(req.body.is_expense==true){
//                     console.log("expense hai");
//                     req.body.amount=-req.body.amount;
//                 }
                
//                 await User.updateOne(
//                     { email: decoded.User_email }, // Filter
//                     { $push: { expenditure_list: req.body },
//                     $inc:{
//                         current_funds :req.body.amount
//                     } } // Update
//                   )
//                   .then(result => {
//                     console.log('Update Result:', result);
//                   })
//                   .catch(err => {
//                     console.error('Error:', err);
//                   });

//                    db_user=await User.find({email:decoded.User_email})


//                 res.json(db_user[0]);

//             }
//         })
//     }
//     else{
//         console.log("you need to sign in");
//     }
// })
app.listen(8000, () => {
    console.log('Server Started on port 8000');
  });
  
