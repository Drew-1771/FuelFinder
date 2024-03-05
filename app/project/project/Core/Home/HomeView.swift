//
//  HomeView.swift
//  project
//
//  Created by Drew S on 3/5/24.
//

import SwiftUI

extension Color {
    init(hex: UInt32) {
        let red = Double((hex & 0xFF0000) >> 16) / 255.0
        let green = Double((hex & 0x00FF00) >> 8) / 255.0
        let blue = Double(hex & 0x0000FF) / 255.0
        self.init(red: red, green: green, blue: blue)
    }
}

struct HomeView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)

    var body: some View {
        VStack{
            HStack() {
                Text("Hello <Username>!")
                    .font(.title)
                    .foregroundColor(textGrey)
                    .frame(alignment: .trailing)
                    .padding()
                Spacer()
                SettingsCog(fgColor: .gray)
            }
            
            HStack {
                VStack(spacing: 20){
                    PreviewBox(color: boxGrey, description: "one")
                    PreviewBox(color: boxGrey, description:  "two")
                    PreviewBox(color: boxGrey, description: "three")
                    Spacer()
                }.padding(.horizontal, 2)
                
                VStack(spacing: 20){
                    PreviewBox(color: boxGrey, description:  "four")
                    PreviewBox(color: boxGrey, description:  "five")
                    PreviewBox(color: boxGrey, description:  "six")
                    Spacer()
                }.padding(.horizontal, 2)
                
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 20)
            
        }.background(Color.black)
    }
}

struct PreviewBox: View {
    var color: Color
    var description: String
    
    var body: some View {
        Button(action: {
            print("selected preview: \(description)")
        }) {
            HStack {
                Image(systemName: "photo.on.rectangle")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 30, height: 30)
                    .padding()
                    .foregroundColor(.white)
                Text(description)
                    .foregroundColor(.white)
                    .padding()
                Spacer()
            }
            .background(color)
            .cornerRadius(10)
        }
    }
}

struct SettingsCog: View {
    var fgColor: Color

    var body: some View {
        Button(action: {
            print("selected settings")
        }) {
            Image(systemName: "gearshape")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 30, height: 30)
                .foregroundColor(fgColor)
                .padding(.horizontal, 25)
        }
    }
}

#Preview {
    HomeView()
}
